import itertools
from datetime import datetime
from typing import List

import openai
import tiktoken
from django.http import JsonResponse
from ninja import Router

from loci.domain import Note
from loci.infra.fetchers.apple import AppleNotesFetcher
from loci.infra.renderers.markdown import MarkDown
from ..dto.common import Result
from ..domain.enum import MemoryType
from ..domain.models import Memory, MemorySyncLog, Neuron, Position
from ..dto.memory import MemoryDTO
from ..domain.manager import MemoryManager


client = openai.OpenAI()
router = Router()


@router.get('/list.json', response=Result[List[MemoryDTO]])
def list_memories(request) -> Result[List[MemoryDTO]]:
    memories = MemoryManager().list_all()

    dto = MemoryDTO.from_model_list(memories)
    
    return Result.with_data(dto)


@router.post('/sync.json', response=Result)
def sync_memories(request):

    markdown = MarkDown()
    fetcher = AppleNotesFetcher(markdown)
    fetcher.start()

    notes = fetcher.notes

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
    return Result.succ()


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