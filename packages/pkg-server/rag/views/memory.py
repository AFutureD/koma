import itertools
from datetime import datetime
from typing import List

from loci.domain.models.note import NoteContentParagraph
import openai
from rag.domain.enum import MemoryType
import tiktoken
from django.http import JsonResponse
from rest_framework import serializers

from loci.domain import Note
from loci.infra.fetchers.apple import AppleNotesFetcher
from loci.infra.renderers.markdown import MarkDown
from ..domain.models import Memory, MemorySyncLog, Neuron, Position
from ..dto.memory import MemoryDTO

client = openai.OpenAI()


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = '__all__'

def list_memories(request):

    memories = Memory.objects.all()

    dto = MemoryDTO.from_model_list(memories)

    return JsonResponse({'data': dto, 'message': None, 'code': 200, 'success': True}, safe = False)


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
        Memory(memory_type = MemoryType.NOTE, data = note.model_dump(mode = 'json'), biz_id = note.uuid)
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


def generate_neurons(note: Note) -> List[Neuron]:

    paragraph_list = note.content.paragraph_list
    if len(paragraph_list) == 0:
        return []
    # check if represent is not blank
    indexable_paragraph = [{"idx":idx, "content": p.represent} for idx, p in enumerate(paragraph_list) if p.represent is not None and not p.represent.isspace()]

    if len(indexable_paragraph) == 0:
        return []

    enc = tiktoken.get_encoding("cl100k_base")
    total_token = sum([len(enc.encode(c["content"])) for c in indexable_paragraph])

    assert total_token <= 8191, "Too many tokens"

    content = [p["content"] for p in indexable_paragraph]
    result = client.embeddings.create(input = content, model = "text-embedding-3-small")

    neurons = [
        Neuron(embedding = data.embedding, content = indexable_paragraph[data.index]["content"], biz_id=note.uuid, position=Position(paragraph=indexable_paragraph[data.index]["idx"]))
        for data in result.data
    ]

    return neurons