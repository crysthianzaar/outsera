FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


FROM base AS test

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

CMD ["pytest", "-v"]


FROM base AS production

EXPOSE 8000
CMD ["sh", "-c", "gunicorn main:app --bind 0.0.0.0:8000 --workers $(($(nproc) * 2 + 1))"]
