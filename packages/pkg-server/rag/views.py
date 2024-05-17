from django.http import HttpResponse, JsonResponse

from django.shortcuts import render
# from django.core import serializers
from rest_framework import serializers
# Create your views here.
from loci.infra.renderers.markdown import MarkDown
from loci.infra.fetchers.apple import AppleNotesFetcher
from rag.models import Memory


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = '__all__'


def index(request):

    markdown = MarkDown()
    fetcher = AppleNotesFetcher(markdown)
    fetcher.start()

    memories = [
        Memory(memory_type = Memory.MemoryType.NOTE, data = note.model_dump(mode = 'json'))
        for note in fetcher.notes
    ]

    serializer = MemorySerializer(memories, many=True)
    return JsonResponse(serializer.data, safe = False)