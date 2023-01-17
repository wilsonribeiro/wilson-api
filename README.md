# Wilson API 
<!-- Lincense -->
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## Introduction:

Docker is one of the most popular containerization technologies. It is a simple-to-use, developer-friendly tool, and has advantages over other similar technologies that make using it smooth and easy. Since its first open-source release in March 2013, Docker has gained attention from developers and ops engineers. According to Docker Inc., Docker users have downloaded over 105 billion containers and "dockerized" 5.8 million containers on Docker Hub. The project has over 32K stars on Github.
Docker has since become mainstream. More than 100K 3rd-party projects are using this technology, and developers with containerization skills are in increasing demand.
Here I will show you, how to use Docker to containerize an application, then how to run it on development environments using Docker Compose. We are going to use a Python API as our main app.
 
## Setting Up a Development Environment:

We are going to install some requirements before starting. We will use a mini Python API here developed in Flask. Flask is a Python framework and is an excellent choice to rapidly prototype an API. Our application will be developed using Flask. If you are not accustomed to Python, you can see the steps to create this API below.
Start by creating a Python virtual environment to keep our dependencies isolated from the rest of the system dependencies. Before this, we will need PIP, a popular Python package manager.
The installation is quite easy, you need to execute the following two commands:

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

For your information, you should have Python 3 installed. You can verify this by typing:

```
python --version
```


‍After installing PIP, use the following command to install the virtual environment:


```
pip install virtualenv
```


## Create the project:

Now lets go create a project for your folder in which you should create a virtual environment, then activate it. Also, create a folder for the app and a file called "app.py".


```
mkdir app
cd app
python3 -m venv venv
. venv/bin/activate
mkdir code
cd code
touch app.py
```



We are going to build a simple API that shows the weather for a given city. For example, if we want to show the weather in Indaiatuba BR, we should request it using the route:


/indaiatuba/br

‍
You need to install the Python dependencies called "flask" and "requests" using PIP. We are going to use them later on:



```bash
pip install flask requests
```



Don't forget to "freeze" your dependencies in a file called "requirements.txt". This file will be used later to install our app dependencies in the container:



```bash
pip freeze > requirements.txt
```
‍


This is what the requirements file looks like: 



```ruby
certifi==2019.9.11
chardet==3.0.4
Click==7.0
Flask==1.1.1
idna==2.8
itsdangerous==1.1.0
Jinja2==2.10.3
MarkupSafe==1.1.1
requests==2.22.0
urllib3==1.25.7
Werkzeug==0.16.0
```



## This is the API initial code:
  

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Wilson API – Works fine!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
```



In order to test it, you need to run python app.py and visit http://127.0.0.1:5000/. You should see "Wilson API – Works fine!" on the web page. We are going to use data from openweathermap.org, so make sure to create an account on the same website and generate an API key.
 
Now, we need to add the convenient code to make the API show weather data about a given city:



```python
import requests

from flask import Flask

app = Flask(__name__)

API_KEY = "45581b696ab5c0011abd67e94508b64c"

@app.route('/')
def index():
    return 'Wilson API – Works fine!'

@app.route('/<string:city>/<string:country>/')
def weather_by_city(country, city):

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = dict(
        q=city + "," + country,
        appid= API_KEY,
    )

    response = requests.get(url=url, params=params)
    data = response.json()
    return data

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
```


Now if you visit 127.0.0.1:5000/indaiatuba/br, you should be able to see a JSON similar to the following one:



```json
{
  "base": "stations",
  "clouds": {
    "all": 90
  },
  "cod": 200,
  "coord": {
    "lat": 51.51,
    "lon": -0.13
  },
```


Our mini API is working. Let's containerize it using Docker.


## Using Docker to Create a Container for our App:

Let's create a container for our API; the first step is creating a Dockerfile. Dockerfile is an instructive text file containing the different steps and instructions that the Docker Daemon should follow to build an image. After building the image, we will be able to run the container.
 
A Dockerfile always starts with the FROM instructions:


```ruby
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
```
‍

In the above file, we did the following things:
 
 - 1. We are using a base image called "python:3".
 - 2. We also set PYTHONUNBUFFERED to 1. Setting PYTHONUNBUFFERED to 1 allows log messages to be dumped to the stream instead of being buffered.
 - 3. We also created the folder /app, and we set it as a workdir.
 - 4. We copied the requirements, then used them to install all the dependencies.
 - 5. We copied all of the files composing our application, namely the app.py file to the workdir.
 - 6. We finally exposed port 5000, since our app will use this port, and we launched the python command with our app.py as an argument. This will start the API when the container starts.
 - 7. We are check the wilson-api is helth with the HELTHCHECK directives. 


After creating the Dockerfile, we need to build it using an image name and a tag of our choice. In our case, we will use "wilson-api" as a name and "v1" as a tag:



```
docker build -t wilson-api:v1 .
```
‍

Make sure that you are building from inside the folder containing the Dockerfile and the app.py file.
 
After building the container, you can run it using:



```
docker run -dit --rm -p 5000:5000 --name weather wilson-api:v1
```
‍


The container will run in the background since we use the -d option. The container is called "weather" (--name weather). It's also reachable on port 5000 since we mapped the host port 5000 to the exposed container port 5000.
 
If we want to confirm the creation of the container, we can use:


```bash
docker ps
```


You should be able to see a very similar output to the following one:



```bash
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS                    NAMES
0e659e41d475        wilson-api:v1          "python app.py"     About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp   weather
```


You should be able to query the API now. Let's test it using CURL.


```
curl http://0.0.0.0:5000/indaiatuba/br/
```


‍If the last command should return a JSON:



```json
{
  "base": "stations",
  "clouds": {
    "all": 90
  },
  "cod": 200,
  "coord": {
    "lat": 51.51,
    "lon": -0.13
}
```


## Using Docker Compose for Development:

Docker Compose is an open-source tool developed by Docker Inc. for defining and running multi-container Docker applications. Docker Compose is also a tool that is meant to be used in development environments, since it allows auto-reloading your container when you update your code, without making you restart your containers manually or rebuilding your image after each change. Without Compose developing using only Docker containers would be frustrating.
For the implementation part, we are going to use a "docker-compose.yml" file.
 
This is the "docker-compose.yml" file we are using with our API:



```yml
version: '3.9'

volumes:
  prometheus_data: {}
  grafana_data: {}

services:

  weather:
    image: wilson-api
    build:
      context: ./
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 15s

  prometheus:
    image: prom/prometheus
    restart: always
    volumes:
      - ./prometheus:/etc/prometheus/
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    ports:
      - 9090:9090
    links:
      - cadvisor:cadvisor
      - alertmanager:alertmanager
    depends_on:
      - cadvisor

  node-exporter:
    image: prom/node-exporter
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - --collector.filesystem.ignored-mount-points
      - '^/(sys|proc|dev|host|etc|rootfs/var/lib/docker/containers|rootfs/var/lib/docker/overlay2|rootfs/run/docker/netns|rootfs/var/lib/docker/aufs)($$|/)'
    ports:
      - 9100:9100
    restart: always
    deploy:
      mode: global

  alertmanager:
    image: prom/alertmanager
    restart: always
    ports:
      - 9093:9093
    volumes:
      - ./alertmanager/:/etc/alertmanager/
    command:
      - '--config.file=/etc/alertmanager/config.yml'
      - '--storage.path=/alertmanager'

  cadvisor:
    image: gcr.io/cadvisor/cadvisor
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    ports:
      - 8080:8080
    restart: always
    deploy:
      mode: global

  grafana:
    image: grafana/grafana
    restart: always
    environment:
      GF_INSTALL_PLUGINS: 'grafana-clock-panel,grafana-simple-json-datasource'
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning/:/etc/grafana/provisioning/
    env_file:
      - ./grafana/config.monitoring
    ports:
      - 3000:3000
    depends_on:
      - prometheus
```



You can see in the above file that I configured the service "weather" to use the image "wilson-api". Map the host port 5000 to the container port 5000 and mount the current folder to the "/app" folder inside the container.
It is also possible to use a Dockerfile instead of an image. This would be recommended in our case since we already have the Dockerfile.
Now simply run "docker-compose up -d" to start running the service or "docker-compose up --build" to build it then run it.



# Conclusion:

In this challeger, we have seen how to create a Docker container for a mini Python API, and we used Docker Compose to create a stack monitoring in development environment for wilson-api.

## A monitoring solution for Docker hosts and containers with:

Prometheus, Grafana, cAdvisor, NodeExporter and alerting with AlertManager.


```
Prometheus:

http://localhost:9090/

http://localhost:9100/metrics

http://localhost:3000/metrics

http://localhost:8080/metrics

http://localhost:9093/metrics

http://localhost:9090/service-discovery?search=
```


```
Node-Exporter:

http://localhost:9100/
```


```
Grafana:

http://localhost:3000
```


```
cAdvisor:

http://localhost:8080/containers/
```


```
Alertmanager:

http://localhost:9093/#/alerts
```


# Autor:

## Wilson Ribeiro

To get information about, take a look at:

    • https://github.com/wilsonribeiro/wilson-api

    • https://www.linkedin.com/in/wilsonribeiro2/
