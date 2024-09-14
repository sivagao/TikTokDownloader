from contextlib import suppress
from sys import platform
from types import SimpleNamespace
from typing import TYPE_CHECKING

from rookiepy import (
    arc,
    brave,
    chrome,
    chromium,
    edge,
    firefox,
    librewolf,
    opera,
    opera_gx,
    vivaldi,
)

from src.custom import INFO
from src.custom import WARNING

if TYPE_CHECKING:
    from src.module import Cookie
    from src.config import Parameter

__all__ = ["Browser"]


class Browser:
    SUPPORT_BROWSER = {
        "Arc": (arc, "Linux, macOS, Windows"),
        "Chrome": (chrome, "Linux, macOS, Windows"),
        "Chromium": (chromium, "Linux, macOS, Windows"),
        "Opera": (opera, "Linux, macOS, Windows"),
        "OperaGX": (opera_gx, "macOS, Windows"),
        "Brave": (brave, "Linux, macOS, Windows"),
        "Edge": (edge, "Linux, macOS, Windows"),
        "Vivaldi": (vivaldi, "Linux, macOS, Windows"),
        "Firefox": (firefox, "Linux, macOS, Windows"),
        "LibreWolf": (librewolf, "Linux, macOS, Windows"),
    }
    PLATFORM = {
        False: SimpleNamespace(
            name="抖音",
            domain=[
                "douyin.com",
            ],
            key="cookie",
        ),
        True: SimpleNamespace(
            name="TikTok",
            domain=[
                "tiktok.com",
            ],
            key="cookie_tiktok",
        ),
    }

    def __init__(self, parameters: "Parameter", cookie_object: "Cookie"):
        self.console = parameters.console
        self.cookie_object = cookie_object

    def run(self, tiktok=False, ):
        options = "\n".join(
            f"{i}. {k}: {v[1]}" for i, (k, v) in enumerate(
                self.SUPPORT_BROWSER.items(), start=1))
        if browser := self.console.input(
                f"读取指定浏览器的 {self.PLATFORM[tiktok].name} Cookie 并写入配置文件\n{options}\n请输入浏览器名称或序号：",
        ):
            if cookie := self.get(browser, self.PLATFORM[tiktok].domain, ):
                self.__save_cookie(cookie, tiktok, )
                self.console.print("读取 Cookie 成功！", style=INFO, )
        else:
            self.console.print("未选择浏览器！")

    def __save_cookie(self, cookie: dict, tiktok: bool):
        self.cookie_object.save_cookie(cookie, self.PLATFORM[tiktok].key)

    def get(self, browser: str | int, domains: list[str], ) -> dict[str, str]:
        if not (browser := self.__browser_object(browser)):
            self.console.print("浏览器名称或序号输入错误！", style=WARNING, )
            return {}
        try:
            cookies = browser(domains=domains)
            return {i["name"]: i["value"] for i in cookies}
        except RuntimeError:
            self.console.print("读取 Cookie 失败，未找到 Cookie 数据！", style=WARNING, )
        return {}

    @classmethod
    def __browser_object(cls, browser: str | int):
        with suppress(ValueError):
            browser = int(browser) - 1
        if isinstance(browser, int):
            try:
                return list(cls.SUPPORT_BROWSER.values())[browser][0]
            except IndexError:
                return None
        if isinstance(browser, str):
            try:
                return cls.__match_browser(browser)
            except KeyError:
                return None
        raise TypeError

    @classmethod
    def __match_browser(cls, browser: str):
        for i, j in cls.SUPPORT_BROWSER.items():
            if i.lower() == browser.lower():
                return j[0]


match platform:
    case "darwin":
        from rookiepy import safari

        Browser.SUPPORT_BROWSER |= {
            "Safari": (safari, "macOS"),
        }
    case "linux":
        Browser.SUPPORT_BROWSER.pop("OperaGX")
    case "win32":
        pass
    case _:
        print("从浏览器读取 Cookie 功能不支持当前平台！")