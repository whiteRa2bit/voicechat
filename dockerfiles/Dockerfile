FROM python:3.8

RUN mkdir /app/
WORKDIR /app/
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y \
    portaudio19-dev

RUN pip install -r requirements.txt

COPY . .
CMD ["/bin/bash"]