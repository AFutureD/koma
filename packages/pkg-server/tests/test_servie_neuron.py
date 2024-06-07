import unittest
from rag.domain.models import Neuron
from rag.infra.services import NeuronService


class NeruonServiceTests(unittest.TestCase):

    def test_neuron_rerank(self):
        
        neurons = [
            Neuron(content = "test1"),
            Neuron(content = "test2"),
            Neuron(content = "great"),
        ]
        result = NeuronService.rerank_neurons(neurons = neurons, query = "test", topk = 2)
        assert len(result) == 2