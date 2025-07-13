FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y gcc libpq-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["./point.sh"]

# внизу всегда должно быть копирование основного приложения иначе при каждом изменении кода будет всё пересобираться
# и заново скачиваться если меняешь requirements то они будут качаться снова потому что после копирования идёт установка
# зависимостей и установиться не только та который не хватает а обсолютно всё заново