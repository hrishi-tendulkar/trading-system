FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY apps ./apps
COPY packages ./packages
COPY services ./services
COPY scripts ./scripts
COPY data ./data

RUN pip install --upgrade pip && pip install .

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
