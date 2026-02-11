FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY section1_script/ ./section1_script/

RUN pip3 install --no-cache-dir -r section1_script/requirements.txt

ENTRYPOINT ["python3", "section1_script/http_requests.py"]

