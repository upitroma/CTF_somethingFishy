FROM alpine:latest

WORKDIR /app

RUN apk update && apk add python3 py3-pip --no-cache make g++ wget ca-certificates

# fetch and compile stockfish
RUN mkdir -p /root/tmp && \
	cd /root/tmp && \
	wget https://github.com/official-stockfish/Stockfish/archive/sf_10.tar.gz && \
	tar xvf /root/tmp/sf_10.tar.gz && \
	cd /root/tmp/Stockfish-sf_10/src && \
	make build ARCH=x86-64-modern && \
	mv /root/tmp/Stockfish-sf_10/src/stockfish /usr/local/bin/stockfish

# remove leftovers
RUN apk del --no-cache wget ca-certificates
RUN rm -rf /root/tmp

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
