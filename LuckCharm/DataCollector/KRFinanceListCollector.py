import requests
from selenium import webdriver
from selenium.webdriver.chrome import options
from LuckCharm.Util.ChromeDriverInstaller import chrome
from time import sleep
from bs4 import BeautifulSoup


def parseFinance():
    map = dict()
    opt = options.Options()
    opt.headless = False
    sel = webdriver.Chrome("../Util/chromedriver.exe", options=opt)
    sel.get(
        "https://kr.investing.com/stock-screener/?sp=country::11|sector::a|industry::a|equityType::a|exchange::a%3Ceq_market_cap;1")

    els = sel.find_element_by_class_name("js-total-results")
    while els.text is "0":
        sleep(0.1)
        # els = sel.find_element_by_class_name("js-total-results")
    total = els.text
    print(els.text + "개의 주식을 찾았습니다. 불러오기를 시작합니다...")
    try:
        while True:
            bs = BeautifulSoup(sel.page_source, "lxml")
            # print(els.find_element_by_css_selector(".resultsContainer"))
            # l1 = els.find_element_by_css_selector("a.pagination")
            l1 = bs.select(".pagination")
            # print(l1)
            li = list()
            page = 0
            for x in l1:
                li.append(int(x.get_text()))
                if x.has_attr("class") and "selected" in x.attrs["class"]:
                    page = int(x.get_text())
            print("페이지 " + str(page) + " 처리중...")
            l1 = bs.select("td[data-column-name=name_trans] > a")
            for x in l1:
                map[x.get_text()] = x.attrs["href"]
            # print(x.get_text())
            print("..." + str(len(map)) + " / " + str(els.text))
            if max(li) is not page:
                sel.get(
                    "https://kr.investing.com/stock-screener/?sp=country::11|sector::a|industry::a|equityType::a"
                    "|exchange::a%3Ceq_market_cap;" + str(
                        page + 1))
                els = sel.find_element_by_class_name("js-total-results")
                while els.text is "0":
                    sleep(0.1)
            else:
                print("모든 페이지를 처리하였습니다. 저장을 시작합니다. (finance_list.csv)")
                break
        sel.quit()
        sel = None
        with open("finance_list.csv", "a", newline='') as ff:
            import csv
            cs = csv.writer(ff)
            for key in map:
                try:
                    print(key)
                    print(map[key])
                    cs.writerow((
                        key, map[key]))
                except Exception as e:
                    pass
    except Exception as e:
        if sel is not None:
            sel.quit()
        sel = None
        raise e


import multiprocessing


def processISIN(processNum: int, file):
    import csv
    _orig = dict()
    with open(file, "rt") as f:
        # print(f.readlines())
        cs = csv.reader(f)
        for x2 in cs:
            _orig[x2[0]] = x2[1]
    print(_orig)
    processes = []
    returns = []
    manager = multiprocessing.Manager()
    _splits = list({y: _orig[y] for y in xx} for xx in split(list(_orig.keys()), processNum))
    for i in range(0, processNum):
        v = manager.dict()
        pr = multiprocessing.Process(
            target=processNetwork,
            args=(i, _splits[i], v)
        )
        returns.append(v)
        processes.append(pr)
        pr.start()
    for pr in processes:
        pr.join()
    print("Complete!")


def split(arr, count):
    return [arr[i::count] for i in range(count)]


import random


def processNetwork(process: int, target: dict, returnVal: dict):
    for key in target:
        try:
            text = requests.get("https://kr.investing.com" + target[key], headers={
                'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}).content
            # print(text)
            bs = BeautifulSoup(
                bytes.decode(text),
                "lxml")
            print(bytes.decode(text))
            print(bs.find_all(".elp"))
            returnVal[key] = bs.find_all("span.elp")[2].get_text()
            print("Discovered " + key + " in process " + str(process) + " : " + returnVal[key])
            # sleep(random.randint(10) * 0.1 + 1)
            return None
        except Exception as e:
            print("Error while process finance " + key)
            raise e
    return returnVal


if __name__ == '__main__':
    # orig = dict()
    # for x in range(40):
    #     orig[x] = x
    # splits = ({y: orig[y] for y in x} for x in split(list(orig.keys()), 6))
    # splits = list(splits)
    # lens = list(len(x) for x in splits)
    # print(lens)
    # print(max(lens))
    # print(min(lens))
    # parseFinance()
    processISIN(6, "finance_list.csv")
    # print(requests.get("https://kr.investing.com/equities/samsung-electronics-co-ltd", headers={
    #     'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}).content)
