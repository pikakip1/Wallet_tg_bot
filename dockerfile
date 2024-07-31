FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=$PYTHONPATH:/app

CMD ["bash", "-c", "ls -la && sleep 10 && alembic revision --autogenerate -m 'init bot' && alembic upgrade head && python3 utils/add_categories.py && python3 main.py"]
