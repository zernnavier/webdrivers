import re
from generic_browser_functions import browser_commands, get_version
from subprocess import run, PIPE
from urllib import request, response
import os


OS = ["", "win", "mac", "linux"]
ARCHITECTURE = ["arm64", "32", "64"]
CHIPSET = ["", "m1"]
CODING_FORMAT = "utf-8"

THIS_FILE_DIRECTORY = os.path.dirname(__file__)
REGEX_VERSION_CAPTURE = r'\d\d*\.\d\d*\.\d\d*\.*\d*'


def main():
    chromeCMDs = browser_commands('google', 'chrome')
    edgeCMDs = browser_commands('microsoft', 'edge')
    firefoxCMDs = browser_commands('mozilla', 'firefox')
    chrome_version, edge_version, firefox_version = get_version(chromeCMDs), get_version(edgeCMDs), get_version(firefoxCMDs)
    if chrome_version is not None:
        os_architecture_chipset = get_os_architecture_chipset(OS[1], ARCHITECTURE[1], CHIPSET[0])
        chrome_update(chrome_version, os_architecture_chipset, THIS_FILE_DIRECTORY)
    else:
        print("Unable to Obtain Google Chrome Browser Version")
    if edge_version is not None:
        os_architecture_chipset = get_os_architecture_chipset(OS[1], ARCHITECTURE[2], CHIPSET[0])
        edge_update(edge_version, os_architecture_chipset, THIS_FILE_DIRECTORY)
    else:
        print("Unable to Obtain Microsoft Edge Browser Version")
    if firefox_version is not None:
        os_architecture_chipset = get_os_architecture_chipset(OS[1], ARCHITECTURE[2], CHIPSET[0])
        gecko_update(firefox_version, os_architecture_chipset, THIS_FILE_DIRECTORY)
    else:
        print("Unable to Obtain Microsoft Edge Browser Version")


def get_os_architecture_chipset(os: str, architecture: str, chipset: str) -> str:
    os_architecture_chipset = ""
    if chipset == "":
        os_architecture_chipset += f'{os}{architecture}'
    else:
        os_architecture_chipset += f'{os}{architecture}_{chipset}'
    return os_architecture_chipset


def get_latest_gecko_driver_version():
    url = "https://github.com/mozilla/geckodriver/releases/latest"
    response = request.urlopen(url)
    redirected_url = response.geturl()
    return re.search(REGEX_VERSION_CAPTURE, redirected_url).group(0)


def driver_version(driver_path) -> str:
    cmds = {
        1: [driver_path, "--version"],
        2: ['FINDSTR', "/R", r'"[0-9][0-9]*[^0-9][0-9][0-9]*[^0-9][0-9][0-9]*[^0-9]*[0-9]*"']
    }
    str_form_cmd = " | ".join([" ".join(cmd) for cmd in cmds.values()])
    stdout = run(str_form_cmd, capture_output=True, shell=True, text=True).stdout.strip()
    return re.search(REGEX_VERSION_CAPTURE, stdout).group(0)
    

def chrome_update(version: str, os_architecture_chipset: str, destination: str):
    driver_path = f'{THIS_FILE_DIRECTORY}\chromedriver.exe'
    if not os.path.exists(driver_path):
        print("Downloading chromedriver.exe")
        os.system(f"Auto-ChromeDriver-Downloader.bat {version} {os_architecture_chipset} {destination}")
        return
    [a, b, c, _] = version.split('.')
    url = f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{a}.{b}.{c}'
    response = request.urlopen(url)
    expected_driver_version = response.read().decode(CODING_FORMAT).strip()
    current_driver_version = driver_version(driver_path)
    if current_driver_version == expected_driver_version:
        print(f"Matching 'chromedriver.exe' already exists in the '{destination}' directory")
        return
    print(f'{current_driver_version = }, {expected_driver_version = }')
    print("Downloading matching chromedriver.exe")
    os.system(f"Auto-ChromeDriver-Downloader.bat {version} {os_architecture_chipset} {destination}")


def edge_update(version: str, os_architecture_chipset: str, destination: str):
    driver_path = f'{THIS_FILE_DIRECTORY}\msedgedriver.exe'
    if not os.path.exists(driver_path):
        print("Downloading msedgedriver.exe")
        os.system(f"Auto-EdgeDriver-Downloader.bat {version} {os_architecture_chipset} {destination}")
        return
    current_driver_version = driver_version(driver_path)
    if current_driver_version == version:
        print(f"Matching 'msedgedriver.exe' already exists in the '{destination}' directory")
        return
    print(f'{current_driver_version = }, expected_driver_{version = }')
    print("Downloading matching msedgedriver.exe")
    os.system(f"Auto-EdgeDriver-Downloader.bat {version} {os_architecture_chipset} {destination}")


def gecko_update(version: str, os_architecture_chipset: str, destination: str):
    driver_path, gecko_version = f'{THIS_FILE_DIRECTORY}\geckodriver.exe', get_latest_gecko_driver_version()
    if not os.path.exists(driver_path):
        print("Downloading geckodriver.exe")
        os.system(f"Auto-GeckoDriver-Downloader.bat {version}:{gecko_version} {os_architecture_chipset} {destination}")
        return
    current_gecko_version = driver_version(driver_path)
    if driver_version(driver_path) == gecko_version:
        print(f"Latest 'geckodriver.exe' already exists in the '{destination}' directory")
        return
    print(f'{current_gecko_version = }, expected_{gecko_version = }')
    print("Downloading latest geckodriver.exe")
    os.system(f"Auto-GeckoDriver-Downloader.bat {version}:{gecko_version} {os_architecture_chipset} {destination}")


if __name__ == "__main__":
    main()
