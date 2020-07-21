from win32api import GetFileVersionInfo, LOWORD, HIWORD

def getVersion(filename):
    try:
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
    except:
        return 0, 0, 0, 0


if __name__ == '__main__':
    import os

    filename = os.environ["COMSPEC"]
    # print(".".join(str(e) for e in get_version_number("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe")))
