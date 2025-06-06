FROM python:3.12-slim

RUN apt-get update && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y gcc libpq-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["./point.sh"]