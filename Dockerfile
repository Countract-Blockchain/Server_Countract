# syntax=docker/dockerfile:1

FROM python:alpine

# set a directory for the app
WORKDIR /python-docker

# copy all the files to container
COPY . .

#install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD [ "python3", "./app.py"]