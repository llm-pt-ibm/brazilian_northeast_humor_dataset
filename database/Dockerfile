FROM python:alpine

RUN apt-get update && apt-get install -y \
    ffmpeg \
    sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "main.py"]