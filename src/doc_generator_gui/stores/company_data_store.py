from ..services.readers import CompanyDataService


class CompanyDataStore:
    def __init__(self):
        self.__companyDataService = CompanyDataService("data/company.json")
        self.__companyData = None

    def getCompanyData(self) -> dict:
        if self.__companyData is None:
            self.__companyData = self.__companyDataService.load()

        return self.__companyData
