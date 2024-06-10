ARG PYTHON_BASE=3.12-slim
FROM python:$PYTHON_BASE AS base

RUN pip install -U 'uvicorn[standard]'
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false

FROM base AS production

COPY pyproject.toml pdm.lock /root/koma/
COPY packages/ /root/koma/packages

WORKDIR /root/koma/packages/pkg-server 
RUN pdm install --check --prod --no-editable

EXPOSE 8000

ENTRYPOINT [ "pdm" ]

CMD ["run", "server"]
