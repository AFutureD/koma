

import itertools
from datetime import datetime
from typing import List

import openai
import tiktoken

from loci.domain.models.note import Note
from loci.infra.fetchers.apple import AppleNotesFetcher
from loci.infra.renderers.markdown import MarkDown

from ..domain.enum import EmbedModel, MemoryType
from ..domain.manager import MemoryManager, MemorySyncLogManager, NeuronManager
from ..domain.models import Memory, MemorySyncLog, Neuron, Position
from ..dto.memory import MemoryDTO, NeuronDTO

client = openai.OpenAI()


class MemoryBizService:

    def list_all(self) -> List[MemoryDTO]:
        memories = MemoryManager().list_all()
        dto = MemoryDTO.from_model_list(memories)
        return dto
    
    def sync_memories(self):

        markdown = MarkDown()
        fetcher = AppleNotesFetcher(markdown)
        fetcher.start()

        notes = fetcher.notes[0:10]

        uuids = list(map(lambda x: x.uuid, notes))
        logs = MemorySyncLogManager().list_by_biz_ids(uuids)

        last_modified_map_by_biz_id = {log.biz_id: log.biz_modified_at for log in logs}

        callback_min = datetime(1970, 1, 1).astimezone()
        to_update_notes = list(filter(
            lambda x: x.modified_at > last_modified_map_by_biz_id.get(x.uuid, callback_min),
            notes
        ))

        if len(to_update_notes) == 0:
            return

        memories = [
            Memory(memory_type = MemoryType.NOTE, data = note, biz_id = note.uuid)
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

        MemoryManager().bulk_create(memories)
        MemorySyncLogManager().bulk_create(sync_logs)
        NeuronManager().bulk_create(neurons)

        return


def generate_neurons(note: Note) -> List[Neuron]:

    paragraph_list = note.content.paragraph_list
    if len(paragraph_list) == 0:
        return []
    # check if represent is not blank
    indexable_paragraph = [
        {"idx":idx, "content": p.represent} 
        for idx, p in enumerate(paragraph_list) 
        if p.represent is not None and not p.represent.isspace()
    ]

    if len(indexable_paragraph) == 0:
        return []

    enc = tiktoken.get_encoding("cl100k_base")
    total_token = sum([len(enc.encode(c["content"])) for c in indexable_paragraph])

    assert total_token <= 8191, "Too many tokens"

    content = [p["content"] for p in indexable_paragraph]
    result = client.embeddings.create(input = content, model = "text-embedding-3-small")

    neurons = [
        Neuron(
            embedding = data.embedding,
            content = indexable_paragraph[data.index]["content"],
            memory_id = note.uuid,
            position = Position(paragraph = indexable_paragraph[data.index]["idx"]),
            embed_model = EmbedModel.OPENAI_TEXT_EMBEDDING_3_SMALL
        )
        for data in result.data
    ]

    return neurons


class NeuronBizSerivces:
    def search_neurons(self, query) -> List[NeuronDTO]:
        if query is None or query == '':
            return []

        result = client.embeddings.create(input = query, model = "text-embedding-3-small")
        embedding = result.data[0].embedding

        neurons = NeuronManager().list_within_distance_on_embedding(embedding = embedding, distance = 0.80)

        return NeuronDTO.from_model_list(neurons)