FROM python:3.11-slim-bullseye

# Define build arguments
ARG API_PORT=8000

# Set environment variables (Docker Compose will override these)
# ENV PYTHONUNBUFFERED=1 \
#     DATABASE_URL=postgresql+psycopg2://postgres:mypassword@db:5432/mydatabase \
#     API_PORT=${API_PORT}

WORKDIR /ftc-video-to-zip-service
RUN pip install poetry==1.8.3
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock README.md alembic.ini ./
COPY alembic/ /ftc-video-to-zip-service/alembic/
COPY scripts/ /ftc-video-to-zip-service/scripts/
COPY src/ /ftc-video-to-zip-service/src/
RUN poetry install --no-dev

RUN chmod +x scripts/api.sh

#EXPOSE ${API_PORT}

#CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
