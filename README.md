# mapproxy

This custom mapproxy repo manages deployment configurations and a docker image, based on the official mapproxy image.


## Environment Variables

Here is a list of important environment variables affecting image build/runtime. Additional variables could be found inside the [Dockerfile](Dockerfile).

`TARGET_BUILD` - selects a mode to start mapproxy  **`nginx`** | `development` | `base`


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

Start the server and uwsgi metrics exporter

```bash
  docker compose up --build
```

Stop the server

```bash
  docker compose down
```