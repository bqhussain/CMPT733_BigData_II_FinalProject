FROM quay.io/bitnami/python:3.8.6-prod-debian-10-r81

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY models/ models/
COPY web_application/ web_application/
COPY data/ data/
COPY run.py .

EXPOSE 5005

CMD ["python", "run.py", "5005"]
