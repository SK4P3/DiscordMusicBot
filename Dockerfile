FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y git && \
    git clone https://github.com/SK4P3/DiscordMusicBot.git .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
