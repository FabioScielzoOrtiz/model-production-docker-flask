# Build the app 
docker build -t madrid-house-prices-app .
docker run -d -p 5000:5000 madrid-house-prices-app

# Save the app as tar file
docker save -o madrid-house-prices-app.tar madrid-house-prices-app

# Anyone with the tar file will be able to run the app as follows:
docker load -i madrid-house-prices-app.tar
docker run -p 5000:5000 madrid-house-prices-app

