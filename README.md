# flask_restful
flask_restful and marshmallow example repository

# Installation

todo

# Running the API

The file `app.py` contains the API itself. All endpoint resources are located in the `endpoints/` directory.

Build the application container:
`docker build -t flask_restful_app app/`

Run the application container:
`docker run -it -p 5000:5000 --rm --name flask_restful_app flask_restful_app ./app.py`

Attach to the running application container:
`docker container exec -it <container_name> /bin/bash`

Make a request to the application container:
`curl -X GET 127.0.0.1:5000/api/v1/version`

# Testing the API

Build the test container:
`docker build -t flask_restful_test test/`

Create bridge network for containers:
`docker network create --driver bridge flask_restful`

Run application container
`docker run -d --rm --name test --network flask_restful --rm --name app flask_restful_app ./app.py`

Get ip of application container:
`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' app`

Run the test container:
`docker run -e API_IP="<ip>" -e API_PORT="5000" -it --rm --name test --network flask_restful flask_restful_test ./test_app.py`

Stop application container:
`docker container stop app`

Stop network:
`docker network rm flask_restful`