import os
import re
from typing import List, Optional, NamedTuple
from subprocess import run

import yaml

from schema import Schema, Regex


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
        application_version_key, version = (
            (f"{application}\\BLBeacon", "version")
            if corporation != "Mozilla"
            else (" ".join((corporation, application)), "CurrentVersion")
        )
        windows_cmds = {
            1: [
                "REG",
                "QUERY",
                f'"HKEY_CURRENT_USER\\SOFTWARE\\{corporation}\\{application_version_key}"',
            ],
            2: ["FINDSTR", f'"{version}"'],
        }
        regex_version_capture = r"\d\d*\.\d\d*\.\d\d*\.*\d*"
        str_form_cmds = [" ".join(j) for i, j in windows_cmds.items()]
        str_form_cmd = " | ".join(str_form_cmds)
        stdout = run(
            str_form_cmd, check=True, capture_output=True, shell=True, text=True
        ).stdout.strip()
        return res.group(0) if (res := re.search(regex_version_capture, stdout)) else None


if __name__ == "__main__":
    main()
