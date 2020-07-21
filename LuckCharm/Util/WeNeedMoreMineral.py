import sys
import os
import subprocess


def elevate():
    try:
        script = os.path.abspath(sys.argv[0])
        params = ''.join([script] + sys.argv[1:] + ['asadmin'])
        print(params)
        subprocess.run(["runas", params])
    except Exception as e:
        print("Error while elevate")


if __name__ == '__main__':
    elevate()
