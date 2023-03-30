# FROM python:3.8-slim
# RUN mkdir /app
# WORKDIR /app
# ADD requirements.txt /app
# RUN pip install -r requirements.txt
# ADD . /app
# EXPOSE 5005
# RUN chmod +x ./entrypoint.sh
# ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "app.wsgi:app"]


FROM python:3.6.7

WORKDIR /usr/src/flask_app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN cat .env