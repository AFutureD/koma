import itertools
from datetime import datetime
from typing import List

import tiktoken
from django.http import JsonResponse
from pgvector.django import L2Distance, CosineDistance
from rest_framework import serializers
import openai
from rest_framework.decorators import api_view

from loci.domain import Note
from loci.infra.fetchers.apple import AppleNotesFetcher
from loci.infra.renderers.markdown import MarkDown
from rag.models import Memory, MemorySyncLog, Neuron

client = openai.OpenAI()


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = '__all__'


class NeuronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neuron
        fields = ['content']


def index(request):

    memories = Memory.objects.all()

    serializer = MemorySerializer(memories, many=True)
    return JsonResponse(serializer.data, safe = False)


def sync_memories(request):

    markdown = MarkDown()
    fetcher = AppleNotesFetcher(markdown)
    fetcher.start()

    notes = fetcher.notes[0:10]

    uuids = list(map(lambda x: x.uuid, notes))
    logs = MemorySyncLog.objects.filter(biz_id__in = uuids)

    last_modified_map_by_biz_id = {log.biz_id: log.biz_modified_at for log in logs}

    callback_min = datetime(1970, 1, 1).astimezone()
    to_update_notes = list(filter(
        lambda x: x.modified_at > last_modified_map_by_biz_id.get(x.uuid, callback_min),
        notes
    ))

    if len(to_update_notes) == 0:
        return JsonResponse({'data': None, 'message': None, 'code': 200, 'success': True})

    memories = [
        Memory(memory_type = Memory.MemoryType.NOTE, data = note.model_dump(mode = 'json'))
        for note in to_update_notes
    ]

    neurons_mapper = map(generate_neurons, to_update_notes)
    nonnull_neurons_mapper = [
        mapper
        for mapper in neurons_mapper
        if mapper is not None
    ]
    neurons = list(itertools.chain.from_iterable(nonnull_neurons_mapper))

    sync_logs = [
        MemorySyncLog(
            biz_id = note.uuid,
            biz_modified_at = note.modified_at
        )
        for note in to_update_notes
    ]

    Memory.objects.bulk_create(memories)
    MemorySyncLog.objects.bulk_create(sync_logs)
    Neuron.objects.bulk_create(neurons)
    return JsonResponse({'data': None, 'message': None, 'code': 200, 'success': True})


def perform(content: List[str], model: str):
    if len(content) == 0:
        return []

    enc = tiktoken.get_encoding("cl100k_base")
    total_token = sum([len(enc.encode(c)) for c in content])

    assert total_token <= 8191, "Too many tokens"

    result = client.embeddings.create(input = content, model = model)

    neurons = [
        Neuron(embedding = data.embedding, content = content[data.index])
        for data in result.data
    ]

    return neurons


def generate_neurons(note: Note) -> List[Neuron]:

    paragraph_list = note.content.paragraph_list
    if len(paragraph_list) == 0:
        return []
    # check if represent is not blank
    paragraph_content = [p.represent for p in paragraph_list if p.represent is not None and not p.represent.isspace()]
    neurons = perform(paragraph_content, model = "text-embedding-3-small")

    return neurons


@api_view(['GET'])
def search_neurons(request):

    query = request.query_params.get('q', None)
    if query is None or query == '':
        return JsonResponse({'data': None, 'message': 'q is required', 'code': 400, 'success': False})

    result = client.embeddings.create(input = query, model = "text-embedding-3-small")
    embedding = result.data[0].embedding
    print(embedding)

    neurons = Neuron.objects.alias(distance = CosineDistance('embedding', embedding)).filter(distance__lt = 0.80)

    serializer = NeuronSerializer(neurons, many = True)
    return JsonResponse({'data': serializer.data, 'message': None, 'code': 200, 'success': True})
