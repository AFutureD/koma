
import openai
from django.http import JsonResponse
from pgvector.django import CosineDistance
from rest_framework import serializers
from rest_framework.decorators import api_view

from ..domain.models import Neuron
from ..dto.memory import NeuronDTO

client = openai.OpenAI()

class NeuronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neuron
        fields = ['content']


@api_view(['GET'])
def search_neurons(request):

    query = request.query_params.get('q', None)
    if query is None or query == '':
        return JsonResponse({'data': None, 'message': 'q is required', 'code': 400, 'success': False})

    result = client.embeddings.create(input = query, model = "text-embedding-3-small")
    embedding = result.data[0].embedding

    neurons = Neuron.objects.alias(distance = CosineDistance('embedding', embedding)).filter(distance__lt = 0.80)

    dto = NeuronDTO.from_model_list(neurons)
    return JsonResponse({'data': dto, 'message': None, 'code': 200, 'success': True})
