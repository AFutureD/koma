from datetime import datetime
import logging

from django.http.response import HttpResponse
from django.http.request import HttpRequest
from ninja import P
from pydantic import BaseModel


class LoggingRecordCxt(BaseModel):
    api: str
    t: datetime
    method: str | None
    param: dict

class LoggingRecordIn(BaseModel):
    context: LoggingRecordCxt
    headers: str
    reqesut: str

class LoggingRecordOut(BaseModel):
    headers: str
    response: str
    t: datetime

class LoggingRecord(BaseModel):
    env: str
    input: LoggingRecordIn
    output: LoggingRecordOut


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.logger.info("RequestLoggingMiddleware initialized")

    def __call__(self, request: HttpRequest):
        
        cxt = LoggingRecordCxt(api=request.path, t=datetime.now(), method=request.method, param={})
        input = LoggingRecordIn(context=cxt, headers=repr(request.headers), reqesut=request.body.decode())

        # core logic
        response: HttpResponse = self.get_response(request)

        output = LoggingRecordOut(headers=repr(response.serialize_headers()), response=response.content.decode(), t=datetime.now())
        record = LoggingRecord(env="", input=input, output=output)

        self.logger.info(record.model_dump_json())

        return response