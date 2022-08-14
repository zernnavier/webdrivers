from typing import Dict, List
from subprocess import run


def main():
    chromeCMDs = browser_commands('google', 'chrome')
    edgeCMDs = browser_commands('microsoft', 'edge')
    firefoxCMDs = browser_commands('mozilla', 'firefox')
    # firefoxCMDs = browser_commands('mozilla', 'mozilla firefox')
    chrome_version, edge_version, firefox_version = get_version(chromeCMDs), get_version(edgeCMDs), get_version(firefoxCMDs)
    print(f'{chrome_version = }', f'{edge_version = }', f'{firefox_version = }', sep="\n")


def browser_commands(corporation: str, software: str) -> Dict[int, List[str]]:
    corporation, software = corporation.strip().title(), software.strip().title()
    if corporation != "Mozilla":
        windows_cmds = {
            1: ['REG', 'QUERY', f'"HKEY_CURRENT_USER\\Software\\{corporation}\\{software}\\BLBeacon"'],
            2: ['FINDSTR', '"version"'],
        }
        return windows_cmds
    actual_software_name = {
        "Firefox": "Mozilla Firefox",
        "Mozilla Firefox": "Mozilla Firefox"
    }
    windows_cmds = {
        1: ['REG', 'QUERY', f'"HKEY_CURRENT_USER\\Software\\{corporation}\\{actual_software_name[software]}"'],
        2: ['FINDSTR', '"CurrentVersion"'],
    }
    return windows_cmds


def get_version(cmds: Dict[int, List[str]]) -> str | None:
    import re
    REGEX_VERSION_CAPTURE = r'\d\d*\.\d\d*\.\d\d*\.*\d*'
    str_form_cmds = [" ".join(j) for i, j in cmds.items()]
    str_form_cmd = " | ".join(str_form_cmds)
    stdout = run(str_form_cmd, capture_output=True, shell=True, text=True).stdout.strip()
    return re.search(REGEX_VERSION_CAPTURE, stdout).group(0)


if __name__ == "__main__":
    main()
