
from typing import List

import openai
from ninja import Router

from ..domain.manager import NeuronManager
from ..dto.common import Result
from ..dto.memory import NeuronDTO
from ..infra.services import NeuronBizSerivces

client = openai.OpenAI()
router = Router()


neuron_biz_services = NeuronBizSerivces()

@router.get('/search.json', response=Result[List[NeuronDTO]])
def search_neurons_json(request, query: str, topk: int = 10) -> Result[List[NeuronDTO]]:
    dto = neuron_biz_services.search_neurons(query=query, topk=topk)
    return Result.with_data(dto)


@router.get('/search.text', response=str)
def search_neurons_text(request, query: str, topk: int) -> str:
    result_str = neuron_biz_services.search_neurons_as_text(query=query, topk=topk)
    return result_str


@router.get('/summrize.text', response=Result[str])
def summrize_neurons(request, query: str) -> Result[str]:
    return Result.with_data("")
