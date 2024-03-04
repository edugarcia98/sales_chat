FROM python:3.10.13-slim-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements/ requirements/

RUN pip install --upgrade pip
RUN pip install -r requirements/default.txt --no-cache-dir

COPY . /src/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
