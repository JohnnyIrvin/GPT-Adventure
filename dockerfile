FROM python:3.11.1-slim as base
WORKDIR /adventure
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m install playwright
COPY adventure/ .
COPY config.json .

FROM base as dev
EXPOSE 8000
ENTRYPOINT ["python", "/adventure"]
