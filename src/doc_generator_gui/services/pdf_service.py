import os
import tempfile

from playwright.sync_api import sync_playwright

from ..contexts.document_context import DocumentContext


class PDFService:
    """
    This class is responsible for generating our PDFs to later
    be printed physically.
    """

    def __init__(self, documentContext: DocumentContext):
        self._documentContext = documentContext

    def generate(self):
        """
        we create a temporary file with the current html store,
        use a Playwright to open a browser and generate the pdf
        from the html.
        """

        with tempfile.NamedTemporaryFile(
            dir="data/templates/",
            mode="w",
            suffix=".html",
            encoding="utf8",
            delete=False,
        ) as tmp:
            tmp.write(self._documentContext.currentHTML)
            file_path = tmp.name

        browsers = [
            ("chrome", "chromium"),
            ("firefox", "firefox"),
            ("msedge", "chromium"),
        ]

        for name, driver in browsers:
            try:
                with sync_playwright() as p:
                    # Attempt to launch a browser
                    browser_type = getattr(p, driver)
                    browser = browser_type.launch(channel=name)

                    page = browser.new_page()

                    file_path = os.path.abspath(file_path)

                    page.goto(f"file:///{file_path}")

                    # Generate PDF with specific format
                    page.pdf(path=self._documentContext.outputPath, format="A4")

                    browser.close()

                    os.remove(file_path)
                    return
            except Exception as e:
                print(f"Browser {name} unavailable: {e}")

        raise Exception("No browser available!")
