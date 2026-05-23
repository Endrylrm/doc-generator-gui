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

    def render(self, file: str, input_data: dict[str, str]):
        """
        this function renders all the template variables in our html
        with the correct data, setting our current html clean and ready
        for use.
        """

        template = self._env.get_template(file)
        self._documentContext.currentHTML = template.render(input_data)
