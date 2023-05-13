FROM python:3-slim

RUN addgroup --system telegen
RUN adduser --system --group telegen
USER telegen

WORKDIR /usr/src/telegen

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade pip
COPY --chown=telegen:telegen requirements.txt requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=telegen:telegen . .

CMD ["python", "./telegen.py"]
