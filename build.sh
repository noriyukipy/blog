# Build HTML from the source directory `src` .
# The built file are placed under `docs` directory.
docker container run -w /work -v $(pwd):/work --rm -it python:3.8.2-buster sh -c " \
    pip install -r requirements.txt && \
    cd src && \
    mkdocs build --site-dir ../docs && \
    cd .. \
"
