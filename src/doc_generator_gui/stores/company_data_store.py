from ..services.readers import ReaderService


class CompanyDataStore:
    def __init__(self, reader: ReaderService):
        self.__companyDataService = reader
        self.__companyData = None

    def getCompanyData(self) -> dict:
        if self.__companyData is None:
            self.__companyData = self.__companyDataService.load()

        return self.__companyData
