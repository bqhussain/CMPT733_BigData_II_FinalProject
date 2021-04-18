FROM quay.io/bitnami/python:3.8.6-prod-debian-10-r81

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/ apps/
COPY data/ data/
COPY app.py .
COPY app_temp.py .

EXPOSE 8088

CMD ["python", "app.py", "8088"]
