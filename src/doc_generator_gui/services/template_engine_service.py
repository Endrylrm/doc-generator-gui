from jinja2 import Environment, FileSystemLoader

from ..contexts.document_context import DocumentContext


class TemplateEngineService:
    """
    This class is responsible for working with the html template
    and cleaning our html for creation of PDFs.
    """

    def __init__(self, documentContext: DocumentContext):
        self._documentContext = documentContext

        self._env = Environment(loader=FileSystemLoader("data/templates"))

    def parse(self, file: str, input_data: dict[str, str]):
        """
        this function changes all the variables in our html with the correct data,
        returning a dictionary containing all cleaned html data.
        """
        template = self._env.get_template("header.html")
        self._documentContext.currentHTML["header"] = template.render(**input_data)

        template = self._env.get_template(file)
        self._documentContext.currentHTML["termo"] = template.render(**input_data)

        template = self._env.get_template("footer.html")
        self._documentContext.currentHTML["footer"] = template.render(**input_data)
