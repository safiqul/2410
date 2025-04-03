# Docker

## Overview

Setting up an application typically involves installing an operating system, configuring dependencies, and ensuring everything runs smoothly on a specific machine. But what happens if you need to move the application to another computer? You’d have to go through the entire setup process again, which can be time-consuming.

Now, imagine a solution where you can package the application along with everything it needs to run and deploy it on any machine, anywhere. That’s exactly what Docker does.

Docker allows you to encapsulate an application, along with its dependencies and configurations, into a portable unit called a container. This container can run consistently across different environments—Windows, macOS, or Linux—without worrying about compatibility issues. Whether you're developing locally or deploying at scale, Docker ensures that your application runs the same way every time.

* [Part 1: Installing Docker](#part-1-installing-docker)
* [Part 2: Running a container from Docker Hub](#part-2-running-a-container-from-docker-hub)
* [Part 3: Dockerize your own application](#part-3-dockerize-your-own-application)

## Learning outcomes

* The basic usage of Docker
* Download and run docker from Docker Hub
* How to dockerize your own application


## Part 1: Installing Docker

Installation steps vary by operating system. Visit [Docker’s official website](https://www.docker.com) for detailed instructions.

For macOS, simply download and install Docker Desktop, which includes both the Docker Daemon (which runs in the background) and the Docker Client (which communicates with the daemon).

Docker Desktop includes:

1. `Docker Daemon (dockerd)` – The core service that runs and manages containers. It is always running.
2. `Docker Client` – Interacts with the Docker Engine via a REST API using a command-line interface. When we run docker run, the client sends these commands to dockerd, which carries them out. 


## Part 2: Running a container from Docker Hub

To verify that Docker is installed correctly, we can run a test container. But where do we get containers?

Docker Hub is a cloud-based registry where users share prebuilt containers. Instead of manually carrying dependencies across machines, you can simply pull containers from Docker Hub on any system that has Docker installed. Let’s start with a basic test container called hello-world. Open a terminal and run:

`docker run hello-world`

This command fetches the hello-world container from Docker Hub and runs it on your machine. If everything is set up correctly, you should see an output message `Hello from Docker`. Read the steps Docker took to generate this output.


```
safiqul% docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
c9c5fd25a1bd: Pull complete 
Digest: sha256:7e1a4e2d11e2ac7a8c3f768d4166c2defeb09d2a750b010412b6ea13de1efb19
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

This confirms that your Docker is installed and functioning properly. From here, you can start exploring more advanced containers and even build your own.

You can run an ubuntu container with: 

`docker run -it ubuntu bash`

```
safiqul% docker run -it ubuntu bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
5b17151e9710: Pull complete 
Digest: sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782
Status: Downloaded newer image for ubuntu:latest
root@b306729c7839:/# 
root@b306729c7839:/# 
root@b306729c7839:/# pwd
/
root@b306729c7839:/# ls
bin   dev  home  media  opt   root  sbin  sys  usr
boot  etc  lib   mnt    proc  run   srv   tmp  var
root@b306729c7839:/# exit
```
`-i` keeps the session open for interaction and `-t` provides a terminal interface. When used together (-it), they enable a fully interactive terminal session inside Docker.

# Part 3: Dockerize your own application

Now that we learned the basics of Docket, let's take the next step--containerzing your own application. This means we're gonna
package all applications with all the dependencies into a docker container.

## Example 1: A simple python app

Let's dockerize our simple python app, `app.py`:

```Python
import os
print ("my first docker image")
print ("current dir", os.getcwd())
```

### Creating a `Dockerfile`

To containerize a simple python application, we need to create a `Dockerfile`---a set of instructions that tells Docker how to build and run our application. Below is a simple example of a Dockerfile for a Python app:


```dockerfile

FROM python:3
WORKDIR /pyapp
COPY . /pyapp
CMD ["python3", "app.py"]
```

 - `FROM python:3` - Uses the official Python 3 image as the base, which comes with Python pre-installed.
 - `WORKDIR /pyapp` - Sets the working directory inside the container to `/pyapp`. Any commands will be executed in this directory.
 - COPY . /pyapp - Copies all files from the current directory on your local machine to /pyapp inside the container.
 - `CMD ["python3", "app.py"]` - Defines the default command to run the application when we start the container. Here, it will run `app.py`



 #### Building and Running the Container

> **Note:** Ensure that `Dockerfile` and `app.py` in the same directory. 


####  Build the Docker Image
Run the following command to create a Docker image (replace myapp with a name of your choice):

```sh
$ docker build -t myapp .
```
This tells Docker to build an image using the instructions in the `Dockerfile`.

#### Run the Container

Once the image is built, run the container with:

```sh
$ docker run myapp
```

This executes the `app.py` in the container and prints the following:

```sh
my first docker image
current dir /pyapp
```

## Example 2: Create a simple flask app

In this example, we will create a simple Flask web application and containerize it using Docker. Flask is a lightweight web framework for Python, and Docker will allow us to package it along with all its dependencies for easy deployment. 

### A simple Flask app

Create a project directory `flaskapp` and then add app.py:

```Python

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

This makes a simple Flask application with one route (`/`) and returns a welcome message. We used host=`0.0.0.0` 
to make the app accessible outside the container.


### Create a virtual environment in your local machine and install Flask

It’s good practice to use a virtual environment to manage your dependencies locally:

```sh
$ python3 -m venv venv
$ source venv/bin/activate  
(venv)$ pip3 install flask
```

### Generate `requirements.txt` for the container

Add installed dependencies into a requirements.txt file:

```sh
(venv)$ pip freeze > requirements.txt
```

The requirements.txt file will contain: 

```
blinker==1.9.0
click==8.1.8
Flask==3.1.0
```

### Create a `.dockerignore` file

To keep the Docker image clean, add a `.dockerignore` file to ignore the following.

```bash
# Ignore virtual environments
venv/

# Ignore Python cache files
__pycache__/
*.pyc
*.pyo

# Ignore version control files
.git/
.gitignore

# Ignore Docker-related files
Dockerfile
.dockerignore
```

### Create the Dockerfile

Now, create a Dockerfile to define how Docker will build and run the app:

```dockerfile

# Use the official Python 3.9 image as a base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /flaskapp

# Copy the requirements file and install dependencies
COPY requirements.txt /flaskapp/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /flaskapp

# Expose the Flask app's port
EXPOSE 8080

# Define the command to run the app
CMD ["python", "app.py"]
```

### Build and Run the Docker Container


#### Build the container
Let's build the image now:

```sh
docker build -t flaskapp .
```

#### Run the container
Now, start the container and map port 8080 from the container to port 8080 on your machine:

```sh
docker run -p 8080:8080 flaskapp
```

#### Test the Flask App

Once the container is running, open your favorite browser and type `http://localhost:8080`


#### Stop the container

You can use docker-desktop application to see the active containers and stop them. Alternatively, Run `docker ps` to find the `container_id` and then run `docker stop <container_id>`. 


## Task: Dockerize your simplewebserver code from Oblig

Now you should be able to containerize your own simplewebserver.