import markdown
import dataclasses
import pathlib


@dataclasses.dataclass
class MetaData:
    title: str
    date: str
    tag: str
    description: str = ""


def get_metadata(markdown_str):
    md = markdown.Markdown(extensions=["meta", "toc"])
    # md.convert returns HTML str, but not used
    md.convert(markdown_str)

    meta = md.Meta
    meta = {key: ", ".join(val) for key, val in meta.items()}

    title = md.toc_tokens[0]["name"]

    return MetaData(title=title, **meta)


def render_metadata(metadata, filename, render_path_prefix):
    fmt = f"""## [{metadata.title}]({render_path_prefix}/{filename})
📅 {metadata.date}
🏷 {metadata.tag}

{metadata.description}
<hr />
    """

    return fmt


def main(doc_dir, render_path_prefix):
    sorted_path = sorted(
        pathlib.Path(doc_dir).iterdir(),
        key=lambda x: x.name,
        reverse=True
    )
    for path in sorted_path:
        with open(path) as f:
            markdown_str = f.read()
            metadata = get_metadata(markdown_str)
            fmt = render_metadata(metadata, path.name, render_path_prefix)
            print(fmt)


if __name__ == "__main__":
    import fire

    fire.Fire(main)