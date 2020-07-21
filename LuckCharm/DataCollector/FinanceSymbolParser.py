import requests
from bs4 import BeautifulSoup
from LuckCharm.Data.APIKey import keys
import json


def parseSymbol(*isin):
    param = list()
    for x in isin:
        param.append({"idType": "ID_ISIN", "idValue": x})
    print(json.dumps(param))
    head = {"Content-Type": "application/json", "X-OPENFIGI-APIKEY": keys().openFIGI()}
    resp = requests.post("https://api.openfigi.com/v2/mapping",
                         data=json.dumps(param), headers=head)
    print(resp)
    return resp.content


if __name__ == '__main__':
    print(parseSymbol("KR7005930003"))
