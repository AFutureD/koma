
import openai
from django.http import JsonResponse
from pgvector.django import CosineDistance
from ninja import Router

from ..domain.models import Neuron
from ..dto.memory import NeuronDTO

client = openai.OpenAI()
router = Router()

@router.post('/search.json')
def search_neurons(request, query: str):

    if query is None or query == '':
        return JsonResponse({'data': None, 'message': 'q is required', 'code': 400, 'success': False})

    result = client.embeddings.create(input = query, model = "text-embedding-3-small")
    embedding = result.data[0].embedding

    neurons = Neuron.objects.alias(distance = CosineDistance('embedding', embedding)).filter(distance__lt = 0.80)

    dto = NeuronDTO.from_model_list(neurons)
    result = list(map(lambda x: x.model_dump(mode='json'), dto))
    return JsonResponse({'data': result, 'message': None, 'code': 200, 'success': True})
