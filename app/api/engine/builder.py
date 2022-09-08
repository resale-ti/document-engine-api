from weasyprint import HTML, CSS
from jinja2 import Environment, BaseLoader


class BuilderEngine:

    def __init__(self, stylesheet_path, header_logo) -> None:
        self.stylesheet_path = stylesheet_path
        self.header_logo = header_logo

    @staticmethod
    def render(data, html) -> str:
        template = Environment(loader=BaseLoader()).from_string(html)
        return template.render(**data)

    @staticmethod
    def generate_pdf_byte(html, default_style) -> bytes:
        return HTML(string=html).write_pdf(target="oi.pdf", stylesheets=[CSS(default_style)])
