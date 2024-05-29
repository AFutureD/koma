from django.test import TestCase

from rag.domain.models import Memory


class LlamaIndexTests(TestCase):
    
    def test_documents(self):
        print(Memory.objects.__dict__)