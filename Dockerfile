FROM python:3.10-bullseye

ADD src requirements.txt /app/
WORKDIR /app

EXPOSE 8081

RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]