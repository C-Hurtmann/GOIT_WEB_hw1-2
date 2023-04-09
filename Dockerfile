FROM python:3.10

ENV bot /interface

WORKDIR ${bot}

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "interface.py"]