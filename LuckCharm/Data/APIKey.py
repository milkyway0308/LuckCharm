class APIKeys:
    def __init__(self):
        self._alphaVantage = "4MVQ5T7SFO6OZ6Z8"
        self._openFIGI = "20eda45e-9376-47c2-873b-5f1c209cb8b6"

    def alphaVantage(self):
        return self._alphaVantage

    def openFIGI(self):
        return self._openFIGI


api = APIKeys()


def keys():
    return api


def updateKeys(target=None):
    global api
    if target is not None:
        api = target
    return api
