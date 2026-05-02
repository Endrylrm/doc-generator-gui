import json


class DocumentContext:
    """
    This class is responsible for providing context on
    data between our printing services.
    """

    def __init__(self):
        """
        Initialization of the DocumentContext Class page.
        """

        self.output_path: str = ""
        self.strings_to_replace: dict[str, str] = {}

        self.ReadCompanyData()

    def ReadCompanyData(self):
        """
        this function reads our company.json, adding data to our strings
        to replace dictionary, then later we use this data to replace the
        html template data and create our PDFs.
        """

        with open("company.json", "r", encoding="utf-8") as company_file:
            company_file_data = json.loads(company_file.read())

        for key in company_file_data.keys():
            replace = company_file_data[key]["replace"]
            value = company_file_data[key]["value"]
            self.strings_to_replace[replace] = value
