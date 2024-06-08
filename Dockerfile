ARG PYTHON_BASE=3.12-slim
FROM python:$PYTHON_BASE AS base

RUN pip install -U 'uvicorn[standard]'
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false

FROM base AS production

ARG PROJECT_DIR=/home/koma/

COPY pyproject.toml pdm.lock $PROJECT_DIR
COPY packages/ $PROJECT_DIR/packages

WORKDIR $PROJECT_DIR/packages/pkg-server 
RUN pdm install --check --prod --no-editable

EXPOSE 8000

CMD ["pdm", "run", "server"]
