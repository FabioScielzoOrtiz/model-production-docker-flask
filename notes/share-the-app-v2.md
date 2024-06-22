# Build the app 
docker build -t madrid-house-prices-app .
docker run -d -p 5000:5000 madrid-house-prices-app

# Tag the Docker Image:
docker tag madrid-house-prices-app fabioscielzoortiz98/madrid-house-prices-app:latest

# Access to your Docker Hub account
docker login

# Push the image
docker push fabioscielzoortiz98/madrid-house-prices-app:latest

# Anyone with access to my Docker Hub repository can pull and run the image
docker pull fabioscielzoortiz98/madrid-house-prices-app:latest
docker run -p 5000:5000 fabioscielzoortiz98/madrid-house-prices-app:latest


############################################################

# Run an already built container 

docker pull DockerHub_username/container_name
docker run -p 8888:8888 DockerHub_username/container_name

Example: official PySpark container

docker pull jupyter/pyspark-notebook
docker run -p 8888:8888 jupyter/pyspark-notebook

Example: a container with my own App

docker pull fabioscielzoortiz98/madrid-house-prices-app:latest
docker run -p 5000:5000 fabioscielzoortiz98/madrid-house-prices-app:latest