class FinanceSymbol:
    def __init__(self, json):
        self._figi = json["figi"]
        self._name = json["name"]
        self._ticker = json["ticker"]
        self._exchCode = json["exchCode"]

    def figi(self):
        return self._figi

    def name(self):
        return self._name

    def ticker(self):
        return self._ticker

    def exchCode(self):
        return self._ticker

    def export(self, fileWriter):
        fileWriter.write(self.figi())