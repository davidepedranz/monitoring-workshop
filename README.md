# Monitoring Workshop

This repository contains the demo presented in the DISI Industrial Workshop at the University of Trento on 9. May 2019. The slides are available [slides.pdf](here).

**Disclaimer**: The setup and the code present in this demo are **NOT** production-ready and do contain serious security problems (missing authentication, too broad privileges, etc.). The demo is for the only purpose of illustrating concepts, patterns and tools useful to implement monitoring in real-world applications. Use it at your own risk!

## Structure

The demo uses Docker Compose to run all the different needed components. Each component is in its own directory at the top level and includes a Dockerfile, needed configuration and, if needed, source code. While it is possible to build and run each components on its own, the best way to run the demo is using Docker Compose.

## Demo

The demo is self-contained and uses Docker containers and Docker Compose.

### Start

Use the following command to start the demo:

```sh
docker-compose build
docker-compose up
```

### Stop

Use the following command to stop the demo:

```sh
docker-compose stop
docker-compose rm -f
```
