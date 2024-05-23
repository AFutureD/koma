
from typing import List
import openai
from django.http import JsonResponse
from pgvector.django import CosineDistance
from ninja import Router

from ..domain.models import Neuron
from ..dto.memory import NeuronDTO
from ..dto.common import Result

client = openai.OpenAI()
router = Router()

@router.post('/search.json', response=Result[List[NeuronDTO]])
def search_neurons(request, query: str) -> Result[List[NeuronDTO]]:

    if query is None or query == '':
        return Result.with_data([])

    result = client.embeddings.create(input = query, model = "text-embedding-3-small")
    embedding = result.data[0].embedding

    neurons = Neuron.objects.alias(distance = CosineDistance('embedding', embedding)).filter(distance__lt = 0.80)

    dto = NeuronDTO.from_model_list(neurons)

    return Result.with_data(dto)
