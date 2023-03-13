FROM python:3-slim

RUN addgroup --system telegpt
RUN adduser --system --group telegpt
USER telegpt

WORKDIR /usr/src/telegpt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade pip
COPY --chown=telegpt:telegpt requirements.txt requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=telegpt:telegpt . .

CMD ["python", "./telegpt.py"]
