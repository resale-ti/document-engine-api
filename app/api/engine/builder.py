from weasyprint import HTML, CSS
import PyPDF2
import os
import io
from pathlib import Path
from jinja2 import Environment, BaseLoader
from api.engine.document_interfaces import HTMLDocument, PDFDocument
import base64


BASE_DIR = Path(__file__).resolve().parent.parent.parent
template_path = os.path.join(
    BASE_DIR, 'static', 'templates', 'regulamento_concorrencia')


class BuilderEngine:

    def build(self, documents: list):
        pdfWriter = PyPDF2.PdfFileWriter()

        # aqui vai ter que separar dentro do for os IF's e arrumar um jeito.
        for document in documents:

            if isinstance(document, HTMLDocument):
                # handle with hmtl - retorna byte e vai fazendo merge
                file_bytes_html = self._handle_with_html(document)
                pypdf_obj = PyPDF2.PdfFileReader(stream=io.BytesIO(initial_bytes=file_bytes_html))

                pdfWriter = self._handle_with_pages(pypdf_obj, pdfWriter)

            elif isinstance(document, PDFDocument):
                # handle with pdf - retorna o byte e vai fazendo merge
                file_bytes_pdf = self._handle_with_pdf(document)
                pypdf_obj = PyPDF2.PdfFileReader(stream=io.BytesIO(initial_bytes=file_bytes_pdf))

                pdfWriter = self._handle_with_pages(pypdf_obj, pdfWriter)

            else:
                raise Exception("Type document not indetified.")

        # Generate just for view - ver uma forma de pegar o bytes desse pdfWriter
        pdfOutputFile = open('MergedFiles.pdf', 'wb')
        pdfWriter.write(pdfOutputFile)

        pdfOutputFile.close()

        return "123"

    def _handle_with_html(self, document):
        default_style = os.path.join(
            document.template_path, document.stylesheets)

        html_template = self.get_html_template(
            document.template_path, document.folder, document.current_layer)

        html = self.render(data=document.data, html=html_template)

        return self.generate_pdf_byte(html=html, default_style=default_style)

    def _handle_with_pdf(self, document):
        pdf_path = Path(os.path.join(document.template_path +
                        f'/{document.folder}', document.current_layer))

        with open(pdf_path, "rb") as pdf_file:
            encoded_string = pdf_file.read()

        return encoded_string

    def _handle_with_pages(self, pypdf_obj, pdfWriter):
        for pageNum in range(pypdf_obj.numPages):
            pageObj = pypdf_obj.getPage(pageNum)
            pdfWriter.addPage(pageObj)

        return pdfWriter

    @staticmethod
    def render(data, html) -> str:
        template = Environment(loader=BaseLoader()).from_string(html)
        return template.render(**data)

    @staticmethod
    def generate_pdf_byte(html, default_style) -> bytes:
        return HTML(string=html).write_pdf(stylesheets=[CSS(default_style)])

    def get_html_template(self, template_path, document_folder, html_filename):
        return Path(os.path.join(template_path + f'/{document_folder}', html_filename)).read_text()
