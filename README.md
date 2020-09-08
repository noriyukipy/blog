# Personal WebPage

## Run local server

```sh
$ docker container run -w /work -v $(pwd):/work --rm -it -p8000:8000 python:3.8.2-buster bash -c "pip install -r requirements.txt && cd src && mkdocs serve --dev-addr 0.0.0.0:8000"
```

Then access to http://localhost:8000

## Blog

Add article and run

```sh
$ python build_blog.py --doc_dir src/docs/blog --render_path_prefix blog >src/docs/blog.md
```

## Build static HTML file

Build HTML file from source file in `src` directory. Output is placed under `docs` directory.

```sh
$ bash build.sh
```

## Directory

### `src/overrides`

Extending theme directory. Current customization enables to show `date` and `tag` meta data in the document.

Read documents for more details
- https://squidfunk.github.io/mkdocs-material/customization/#overriding-blocks
- https://github.com/mkdocs/mkdocs/blob/a4eb4eb42be5b2b7f401f51baf8c0863f54fe63d/docs/user-guide/custom-themes.md 