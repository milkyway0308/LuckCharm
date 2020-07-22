import os.path
import os
from LuckCharm.Util.VersionParser import getVersion
import requests
from bs4 import BeautifulSoup as bs
import tempfile
import shutil
import zipfile
from selenium import webdriver
from LuckCharm.Util.WeNeedMoreMineral import elevate
from selenium.webdriver.chrome.options import Options


class ChromeDirectory:
    chromeDir = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    chromeDriverDir = "C:/Program Files/DevSkywolf/"
    initialize = False


def chrome():
    if not ChromeDirectory.initialize:
        elevate()
        checkChromeDriver(ChromeDirectory.chromeDriverDir)
        ChromeDirectory.initialize = True
    opt = Options()
    opt.headless = True
    return webdriver.Chrome(ChromeDirectory.chromeDriverDir + "chromedriver.exe", options=opt)


def checkChromeDriver(chromeDriverFile):
    print("Checking for Chrome on default root")
    if not os.path.isfile(ChromeDirectory.chromeDir):
        ChromeDirectory.chromeDir = input(
            "Chrome not installed on default directory. Please enter chrome directory manually.\nChrome directory: ")
        if not ChromeDirectory.chromeDir.endswith(".exe"):
            if not ChromeDirectory.chromeDir.endswith("/"):
                ChromeDirectory.chromeDir += "chrome.exe"
            else:
                ChromeDirectory.chromeDir += "/chrome.exe"
        print("...Cheking chrome installation")
        if not os.path.isfile(ChromeDirectory.chromeDir):
            raise FileNotFoundError("Error: Chrome not installed")
    print("Checking for ChromeDriver..")
    realDriver = chromeDriverFile + "/chromedriver.exe"
    if os.path.isfile(realDriver):
        print("...ChromeDriver found.")
        print("Checking for ChromeDriver version")
        opt = Options()
        opt.headless = True
        chr = webdriver.Chrome(realDriver, options=opt)
        cVer = list(int(x) for x in chr.capabilities['chrome']['chromedriverVersion'].split(" ")[0].split("."))
        chr.close()
        print("...ChromeDriver version: " + ".".join(str(e) for e in cVer))
        print("Checking for Chrome version")
        chVer = getVersion(ChromeDirectory.chromeDir)
        print("...Chrome version: " + ".".join(str(e) for e in chVer))
        if cVer[0] is not chVer[0]:
            print("...ChromeDriver version mismatch!")
            print("Deleting ChromeDriver...")
            shutil.rmtree(chromeDriverFile)
            print("...Complete.")
        else:
            print("...ChromeDriver version match.")
            return None
    else:
        print("...ChromeDriver not found.")
        print("Checking for Chrome version")
        chVer = getVersion(ChromeDirectory.chromeDir)
    installChromeDriver(chromeDriverFile, chVer[0])


def installChromeDriver(dir, version):
    print("Installing ChromeDriver...")
    print("Target chrome version: " + str(version))
    print("Getting version info from ChromeDriver web page...")
    html = requests.get('https://chromedriver.chromium.org/downloads')

    bb = bs(html.content, 'html.parser')
    sels = bb.select("div > h2 > span > a")
    versionMapping = {int(target.next.split(" ")[1].split(".")[0]): (target.next.split(" ")[1], target["href"]) for
                      target in sels}
    print("...Version found: " + ", ".join(str(x) for x in versionMapping.keys()))
    if version in versionMapping:
        print("...Version match! Downloading ChromeDriver version " + versionMapping[version][0])
        print("Dowloading...")
        dirPath = tempfile.mkdtemp()
        entry = None
        next = None
        zip = None
        try:
            if not os.path.isdir(dir):
                os.makedirs(dir)
            file = dirPath + "/item.zip"
            fl = open(file, "wb")
            fl.write(requests.get("https://chromedriver.storage.googleapis.com/" + versionMapping[
                version][0] + "/chromedriver_win32.zip").content)
            fl.close()
            print("Download complete.")
            print("Extrating from zip...")
            zip = zipfile.ZipFile(file, 'r')
            size = zip.getinfo("chromedriver.exe").file_size
            size = float(size)
            entry = zip.open("chromedriver.exe")
            next = open(dir + "/chromedriver.exe", "wb")
            offset = 0
            for b in entry:
                next.write(b)
                offset += 1
                pctg = float(offset) / size * 10
                pctg = int(pctg)
                if pctg % 10 is 0 and pctg is not 0:
                    print("..." + str(pctg) + "%")

            print("...Download compete.")
        except Exception as err:
            if entry is not None:
                entry.close()
            if next is not None:
                next.close()
            if zip is not None:
                zip.close()
            shutil.rmtree(dirPath)
            raise err
        if entry is not None:
            entry.close()
        if next is not None:
            next.close()
        if zip is not None:
            zip.close()
        shutil.rmtree(dirPath)

    else:
        raise Exception(
            "Error: No matching ChromeDriver version from Chrome " + version + " on official ChromeDriver website")


if __name__ == '__main__':
    chrome().close()
