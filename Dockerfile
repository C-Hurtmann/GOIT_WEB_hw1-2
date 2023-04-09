FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "bot/interface.py"]