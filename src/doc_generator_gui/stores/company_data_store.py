from ..services.readers import CompanyDataService


class CompanyDataStore:
    def __init__(self):
        self.__company_data_service = CompanyDataService("data/company.json")
        self.__company_data = None

    def GetCompanyData(self) -> dict:
        if self.__company_data is None:
            self.__company_data = self.__company_data_service.Load()

        return self.__company_data
