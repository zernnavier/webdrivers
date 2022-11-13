import os
import re
from winreg import OpenKey, HKEY_CURRENT_USER, KEY_READ, QueryValueEx
from typing import List, Optional, NamedTuple

import yaml

from schema import Schema, Regex


REGEX_VERSION_CAPTURE = r"\d+\.\d+\.\d+\.*\d*"


class Browser(NamedTuple):
    corporation: str
    application: str


BrowserList = List[str]


def main():
    browser_corps = {"chrome": "google", "edge": "microsoft", "firefox": "mozilla"}
    browsers = Browsers.get_browsers("config.yaml")
    for browser in browsers:
        browser_obj = Browser(browser_corps[browser], browser)
        version = Browsers.get_version(browser_obj.corporation, browser_obj.application)
        print(f"{version = }")


class Browsers:
    SCHEMA = Schema(
        {
            "BROWSERS": [
                Regex(
                    r"(CHROME|FIREFOX|EDGE)",
                    flags=re.I,
                )
            ]
        }
    )

    @classmethod
    def get_browsers(cls, filename: "os.PathLike") -> "BrowserList":
        with open(filename, "r") as yamlfile:
            configuration = yaml.safe_load(yamlfile)
        cls.SCHEMA.validate(configuration)
        browsers = []
        for browser in configuration["BROWSERS"]:
            if browser not in browsers:
                browsers.append(browser.lower())
        return browsers

    @staticmethod
    def get_version(corporation: str, application: str) -> Optional[str]:
        corporation, application = (
            corporation.strip().title(),
            application.strip().title(),
        )
        application_version_key, version_key = (
            (f"{application}\\BLBeacon", "version")
            if corporation != "Mozilla"
            else (" ".join((corporation, application)), "CurrentVersion")
        )
        with OpenKey(
            key=HKEY_CURRENT_USER,
            sub_key=f"SOFTWARE\\{corporation}\\{application_version_key}",
            access=KEY_READ,
        ) as key:
            version, _ = QueryValueEx(key, version_key)
        return (
            res.group(0) if (res := re.search(REGEX_VERSION_CAPTURE, version)) else None
        )


if __name__ == "__main__":
    main()
