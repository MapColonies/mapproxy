# mapproxy

This custom mapproxy repo manages deployment configurations and a docker image build instructions, based on the official mapproxy image. This repo holds as well configurations for nginx, as a web server before the mapproxy app. The app itself is built from WSGI (uWSGI) and the mapproxy web app. For our use case we chose to use the base image of mapproxy as the source for this app image. This might change in the future as the other flavors evolve.


## Environment Variables

Here is a list of important environment variables affecting image build/runtime. Additional variables could be found inside the [Dockerfile](Dockerfile).

### Build Time

**PATCH_FILES** - select if mapproxy's source should be patched with changes defined in this repo  **`true`** | `false`


## Run Locally

Clone the project

```bash
  git clone https://github.com/MapColonies/mapproxy.git
```

Go to the project directory

```bash
  cd mapproxy
```

Change volume to point to a mapproxy configuration file in [docker-compose.yml](docker-compose.yml)

Start the mapproxy app

```bash
  docker compose up --build
```

Stop the app

```bash
  docker compose down
```