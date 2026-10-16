# Environment Setup

## RabbitMQ

- download and install docker
  - windows: https://docs.docker.com/desktop/setup/install/windows-install/
- start the container for rabbitmq

```bash

# start the rabbitmq container
> docker compose up -d

# check the status of container
> docker container ls

# stop the containers but do not delete the images
> docker compose down

# stop the containers and delete the images
> docker compose down --rmi all

```
