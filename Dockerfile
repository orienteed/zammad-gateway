FROM python:3.10-bullseye

ADD src/ requirements.txt /app/
WORKDIR /app

EXPOSE 8080

RUN pip install -r requirements.txt
CMD ["python", "src/main.py"]