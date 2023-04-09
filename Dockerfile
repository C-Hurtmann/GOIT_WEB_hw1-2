FROM python:3.10

WORKDIR /GOIT_WEB_hw1

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "interface.py"]