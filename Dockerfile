FROM python:3.10

COPY . .
RUN pip install -r requirements.txt

WORKDIR /
ENTRYPOINT python flask_server.py
CMD ["python", "-u", "flask_server.py"]