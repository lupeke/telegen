FROM python:3-slim

# Flush output to stdout and stderr streams
ENV PYTHONUNBUFFERED 1
# Disable writing bytecode files (.pyc) to disk
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/local/src

# Copy and install application requirements
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Use Tini to handle multiple processes
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/local/bin/tini
RUN chmod +x /usr/local/bin/tini
ENTRYPOINT ["tini", "--"]

COPY . .

CMD ["./start.sh"]
