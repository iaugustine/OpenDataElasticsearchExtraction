FROM python:3.8

WORKDIR /app

COPY . /app
RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
RUN pip install -r requirements.txt



ENTRYPOINT ["python", "src/main.py"]