FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1 
CMD [ "python", "app.py" ]