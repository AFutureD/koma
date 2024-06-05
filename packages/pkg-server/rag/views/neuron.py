
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

@router.post('/search.json', response=Result[List[NeuronDTO]])
def search_neurons_json(request, query: str) -> Result[List[NeuronDTO]]:

    dto = neuron_biz_services.search_neurons(query)

    return Result.with_data(dto)


@router.post('/search.text', response=Result[str])
def search_neurons_text(request, query: str) -> Result[str]:
    return Result.with_data("")


@router.post('/summrize.text', response=Result[str])
def summrize_neurons(request, query: str) -> Result[str]:
    return Result.with_data("")
