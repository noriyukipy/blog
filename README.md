# Personal WebPage

## Run local server

```sh
$ docker container run -w /work -v $(pwd):/work --rm -it -p8000:8000 python:3.8.2-buster bash -c "pip install -r requirements.txt && cd src && mkdocs serve --dev-addr 0.0.0.0:8000"
```

Then access to http://localhost:8000

## Build static HTML file

Build HTML file from source file in `src` directory. Output is placed under `docs` directory.

```sh
$ bash build.sh
```
