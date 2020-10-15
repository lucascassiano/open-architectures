# Requirements (all)

| OS      | version     | supported  |
| :--------- | :----------: | :--------: |
| Ubuntu | 20.04   | ✅  |
| MacOS  | 10.15.6 | ✅  |

## [Docker](https://docs.docker.com/engine/install/)

Docker Engine to run the application micro-services as containers.

## [Docker-Compose](https://docs.docker.com/compose/install/)

Docker Compose is used to simplify the develop/deploy process, will also help orchestrate the networks and volumes.

## *(dev only)* [Docker Desktop (MacOS only)](https://docs.docker.com/docker-for-mac/install/)

Docker Dashboard for MacOS and Windows (windows will *not* be supported, due to I'm too lazy to turn on my PC, Microsoft Windows = 💩design.)

## *(dev only)* [DockerStation](https://dockstation.io/)

This will work for most Operating Systems, highly helpful to control all containers from a GUI. It can also be used to manage a remote server. See [docker-compose  references](https://docs.docker.com/compose/compose-file/) for more info.

# Architecture

The easiest way to see how this system works is on `docker-compose.yml` . There you can see all the images that will be built, networks, volumes, environment variables, etc.

| service     | directory    | summary  |
| :--------- | :---------- | :-------- |
| reverse-proxy | ./reverse-proxy   | Will do all the reverse-proxy  |
| **server**  | ./server|  Main Server, **Flask** |
| mongo  | - |  Main Database, used for users authentication |
| streamlit-app  | ./streamlit-app |  Simple [Streamlit](https://www.streamlit.io/) app, for interactive **Data Visualizations**|
| vue-app | ./vue-app | Simple [Vue](https://vuejs.org/) App, for **WebApp** |

# Running

``` sh
cd ./a0
docker-compose up
```
