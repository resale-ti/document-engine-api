from weasyprint import HTML, CSS
import PyPDF2
import os
import io
import requests
from pathlib import Path
from jinja2 import Environment, BaseLoader
from api.engine.document_interfaces import HTMLDocument, PDFDocument, PDFLinkDocument
from celery import current_task



BASE_DIR = Path(__file__).resolve().parent.parent.parent
template_path = os.path.join(BASE_DIR, 'static', 'templates', 'regulamento_concorrencia')


class BuilderEngine:

    def __init__(self) -> None:
        self.pdfWriter = PyPDF2.PdfFileWriter()
        self.file_name = current_task.request.id if current_task else 'MergedFiles'

    def _handle_file_bytes(self, file_bytes):
        pypdf_obj = PyPDF2.PdfFileReader(stream=io.BytesIO(initial_bytes=file_bytes))

        self._handle_with_pages(pypdf_obj)

    def _generate_pdf_file(self):
        pdfOutputFile = open(f'{self.file_name}.pdf', 'wb')
        self.pdfWriter.write(pdfOutputFile)
        pdfOutputFile.close()


    def _handle_with_html(self, document):
        default_style = os.path.join(document.template_path, document.stylesheets)

        html = self._generate_html_with_data(document)

        return self.generate_pdf_byte(html=html, default_style=default_style)

    def _handle_with_pdf(self, document):
        pdf_path = Path(os.path.join(document.template_path +
                        f'/{document.folder}', document.current_layer))

        with open(pdf_path, "rb") as pdf_file:
            encoded_string = pdf_file.read()

        return encoded_string

    def _handle_with_pdf_link(self, document):
        pdf = requests.get(document.url_layer, stream=True)
        return pdf.content

    def _handle_with_pages(self, pypdf_obj):
        self.pdfWriter.append_pages_from_reader(pypdf_obj)

    def _handle_with_instances(self, document):
        if isinstance(document, HTMLDocument):
            file_bytes = self._handle_with_html(document)

        elif isinstance(document, PDFDocument):
            file_bytes = self._handle_with_pdf(document)

        elif isinstance(document, PDFLinkDocument):
            file_bytes = self._handle_with_pdf_link(document)

        else:
            raise Exception("Type document not indetified.")

        return file_bytes

    def _generate_html_with_data(self, document):
        folder = document.folder if hasattr(document, 'folder') else ""

        html_template = self.get_html_template(
            document.template_path, folder, document.current_layer)

        document_data = document.data if hasattr(document, 'data') else {}

        html = self.render(data=document_data, html=html_template)

        return html

    def _get_file_bytes_pdf_writer(self):
        # Se for LOCAL arquivo será criado na pasta app
        erase_file = False if (os.environ.get("STAGE")).upper() == "LOCAL" else True

        pdfOutputFile = open(f'{self.file_name}.pdf', 'wb')
        self.pdfWriter.write(pdfOutputFile)

        pathOutputFile = os.path.realpath(pdfOutputFile.name)
        pdfOutputFile.close()

        with open(pathOutputFile, "rb") as pdf_file:
            encoded_string = pdf_file.read()

        if erase_file and os.path.isfile(pathOutputFile):
            os.remove(pathOutputFile)

        return encoded_string

    @staticmethod
    def render(data, html) -> str:
        template = Environment(loader=BaseLoader()).from_string(html)
        return template.render(**data)

    @staticmethod
    def generate_pdf_byte(html, default_style=False) -> bytes:
        if default_style:
            return HTML(string=html).write_pdf(stylesheets=[CSS(default_style)])
        else:
            return HTML(string=html).write_pdf()

    @staticmethod
    def get_html_template(template_path, document_folder, html_filename):
        return Path(os.path.join(template_path + f'/{document_folder}', html_filename)).read_text()
