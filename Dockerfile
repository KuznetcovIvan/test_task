FROM python:3.10
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv --no-cache-dir && uv sync --no-group dev --group prod --frozen
COPY . .
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
