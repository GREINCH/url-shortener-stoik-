FROM python:3.10-slim

WORKDIR /var/api

COPY ./api .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/var/api"

EXPOSE 80

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
