import re
import os
import shutil
from io import BytesIO
from subprocess import run
from urllib import request
from zipfile import ZipFile

from generic_browser_functions import Browser, Browsers


THIS_FILE_DIRECTORY = os.path.dirname(__file__)


def main():
    downloader = DriverDownloader()
    browser_corps = {"chrome": "google", "edge": "microsoft", "firefox": "mozilla"}
    browsers = Browsers.get_browsers("config.yaml")
    for browser in browsers:
        browser_obj = Browser(browser_corps[browser], browser)
        version = Browsers.get_version(browser_obj.corporation, browser_obj.application)
        if version is not None:
            getattr(downloader, f"{browser}_update")(version, THIS_FILE_DIRECTORY)
        else:
            print(
                "Unable to Obtain "
                f"{browser_obj.corporation.title()} {browser_obj.application.title()}"
                " Browser Version"
            )


class DriverDownloader:
    OS = ["", "win", "mac", "linux"]
    ARCHITECTURE = ["arm64", "32", "64"]
    CHIPSET = ["", "m1"]
    CODING_FORMAT = "utf-8"
    REGEX_VERSION_CAPTURE = r"\d\d*\.\d\d*\.\d\d*\.*\d*"
    CHROME_VERSION_URL = (
        r"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_major.minor.state"
    )
    CHROME_DOWNLOAD_URL = (
        r"https://chromedriver.storage.googleapis.com/version/chromedriver_platform.zip"
    )
    GECKO_VERSION_URL = r"https://github.com/mozilla/geckodriver/releases/latest"
    GECKO_DOWNLOAD_URL = (
        "https://github.com/mozilla/geckodriver/releases/download/"
        "vversion/geckodriver-vversion-platform.zip"
    )
    EDGE_DOWNLOAD_URL = (
        r"https://msedgedriver.azureedge.net/version/edgedriver_platform.zip"
    )

    @classmethod
    def _get_chrome_version_url(cls, **kwargs) -> str:
        for key, value in kwargs.items():
            cls.CHROME_VERSION_URL = cls.CHROME_VERSION_URL.replace(key, value)
        return cls.CHROME_VERSION_URL

    @classmethod
    def _get_chrome_download_url(cls, **kwargs) -> str:
        for key, value in kwargs.items():
            cls.CHROME_DOWNLOAD_URL = cls.CHROME_DOWNLOAD_URL.replace(key, value)
        return cls.CHROME_DOWNLOAD_URL

    @classmethod
    def _get_gecko_download_url(cls, **kwargs) -> str:
        for key, value in kwargs.items():
            cls.GECKO_DOWNLOAD_URL = cls.GECKO_DOWNLOAD_URL.replace(key, value)
        return cls.GECKO_DOWNLOAD_URL

    @classmethod
    def _get_edge_download_url(cls, **kwargs) -> str:
        for key, value in kwargs.items():
            cls.EDGE_DOWNLOAD_URL = cls.EDGE_DOWNLOAD_URL.replace(key, value)
        return cls.EDGE_DOWNLOAD_URL

    @classmethod
    def _get_os_architecture_chipset(
        cls, os_name: str, architecture: str, chipset: str
    ) -> str:
        os_architecture_chipset = ""
        if chipset == "":
            os_architecture_chipset += f"{os_name}{architecture}"
        else:
            os_architecture_chipset += f"{os_name}{architecture}_{chipset}"
        return os_architecture_chipset

    @classmethod
    def _get_latest_gecko_driver_version(cls):
        with request.urlopen(cls.GECKO_VERSION_URL) as response:
            redirected_url = response.geturl()
        return re.search(cls.REGEX_VERSION_CAPTURE, redirected_url).group(0)

    @classmethod
    def _driver_version(cls, driver_path: "os.PathLike") -> str:
        window_cmd = {
            1: [driver_path, "--version"],
            2: [
                "FINDSTR",
                "/R",
                r'"[0-9][0-9]*[^0-9][0-9][0-9]*[^0-9][0-9][0-9]*[^0-9]*[0-9]*"',
            ],
        }
        str_form_cmd = " | ".join([" ".join(cmd) for cmd in window_cmd.values()])
        stdout = run(
            str_form_cmd, check=True, capture_output=True, shell=True, text=True
        ).stdout.strip()
        return re.search(cls.REGEX_VERSION_CAPTURE, stdout).group(0)

    @staticmethod
    def _download_and_extract_zip(url: str, destination: "os.PathLike"):
        with request.urlopen(url) as response:
            with ZipFile(BytesIO(response.read())) as zipfile:
                zipfile.extractall(path=destination)
        driver_notes = f'{destination}{os.sep}Driver_Notes{os.sep}'
        if os.path.exists(driver_notes):
            shutil.rmtree(driver_notes)

    def _chrome_driver_download(
        self, version: str, platform: str, destination: "os.PathLike"
    ):
        url = self._get_chrome_download_url(version=version, platform=platform)
        self._download_and_extract_zip(url, destination)

    def _edge_driver_download(
        self, version: str, platform: str, destination: "os.PathLike"
    ):
        url = self._get_edge_download_url(version=version, platform=platform)
        self._download_and_extract_zip(url, destination)

    def _gecko_driver_download(
        self, version: str, platform: str, destination: "os.PathLike"
    ):
        url = self._get_gecko_download_url(version=version, platform=platform)
        self._download_and_extract_zip(url, destination)

    def chrome_update(self, version: str, destination: "os.PathLike"):
        [major, minor, state, _] = version.split(".")
        url = self._get_chrome_version_url(major=major, minor=minor, state=state)
        with request.urlopen(url) as response:
            expected_driver_version = response.read().decode(self.CODING_FORMAT).strip()
        platform = self._get_os_architecture_chipset(
            self.OS[1], self.ARCHITECTURE[1], self.CHIPSET[0]
        )
        driver_path = f"{destination}{os.sep}chromedriver.exe"
        if not os.path.exists(driver_path):
            print("Downloading chromedriver.exe")
            self._chrome_driver_download(expected_driver_version, platform, destination)
            return
        current_driver_version = self._driver_version(driver_path)
        if current_driver_version == expected_driver_version:
            print(
                f"Matching 'chromedriver.exe' already exists in the '{destination}' directory"
            )
            return
        print(f"{current_driver_version = }, {expected_driver_version = }")
        print("Updating matching chromedriver.exe")
        self._chrome_driver_download(expected_driver_version, platform, destination)

    def edge_update(self, version: str, destination: "os.PathLike"):
        platform = self._get_os_architecture_chipset(
            self.OS[1], self.ARCHITECTURE[2], self.CHIPSET[0]
        )
        driver_path = f"{destination}{os.sep}msedgedriver.exe"
        if not os.path.exists(driver_path):
            print("Downloading msedgedriver.exe")
            self._edge_driver_download(version, platform, destination)
            return
        current_driver_version = self._driver_version(driver_path)
        if current_driver_version == version:
            print(
                f"Matching 'msedgedriver.exe' already exists in the '{destination}' directory"
            )
            return
        print(f"{current_driver_version = }, expected_driver_{version = }")
        print("Downloading matching msedgedriver.exe")
        self._edge_driver_download(version, platform, destination)

    def gecko_update(self, version: str, destination: "os.PathLike"):
        platform = self._get_os_architecture_chipset(
            self.OS[1], self.ARCHITECTURE[2], self.CHIPSET[0]
        )
        driver_path = f"{destination}{os.sep}geckodriver.exe"
        gecko_version = self._get_latest_gecko_driver_version()
        if not os.path.exists(driver_path):
            print("Downloading geckodriver.exe")
            self._gecko_driver_download(gecko_version, platform, destination)
            return
        current_gecko_version = self._driver_version(driver_path)
        if self._driver_version(driver_path) == gecko_version:
            print(
                f"Latest 'geckodriver.exe' already exists in the '{destination}' directory"
            )
            return
        print(f"{current_gecko_version = }, expected_{gecko_version = }")
        print("Downloading latest geckodriver.exe")
        self._gecko_driver_download(gecko_version, platform, destination)

    def firefox_update(self, version: str, destination: "os.PathLike"):
        self.gecko_update(version, destination)


if __name__ == "__main__":
    main()
