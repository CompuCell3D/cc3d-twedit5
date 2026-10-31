from pathlib import Path

from jinja2 import Environment, StrictUndefined


def render_j2_template(source_template, target_path, substitutions):
    """Render a UTF-8 Jinja2 template to a UTF-8 target file."""
    source_template = Path(source_template)
    target_path = Path(target_path)

    environment = Environment(
        autoescape=False,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    template = environment.from_string(source_template.read_text(encoding="utf-8"))
    target_path.write_text(template.render(**substitutions), encoding="utf-8")
