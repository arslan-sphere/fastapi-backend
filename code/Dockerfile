FROM python:3.10

WORKDIR ./code

COPY ./code/requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]