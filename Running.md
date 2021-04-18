## How to run on local machine using Docker registry
```
docker run -p 5005:5005 -d --name mimic_app ghcr.io/qyune/mimic_app:v1
docker run -p 8088:8088 -d --name mimic_web ghcr.io/qyune/mimic_web:v1
```
