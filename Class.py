from time import sleep
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup
from requests import get
from playwright.sync_api import Page


def GetState(page):
    while page.request.get(page.url).status != 200:
        pass


class GetIdSubjects:
    def __init__(self, page: Page, user, password, unvercity="seu"):
        self.name_id = None
        self.page = page
        self.user = user
        self.password = password
        self.unvercity = unvercity
        self.timeout = 99999999

        if self.unvercity == "seu":
            self.page.goto(
                "https://lms.seu.edu.sa/webapps/bb-auth-provider-cas-BBLEARN/execute/casLogin?cmd=login&authProviderId=_105_1&redirectUrl=https%3A%2F%2Flms.seu.edu.sa%2Fwebapps%2Fportal%2Fexecute%2FdefaultTab",
                timeout=self.timeout,
            )

            self.page.fill(selector='input[id="username"]', value=self.user)
            self.page.fill(selector='input[id="password"]', value=self.password)
            self.page.click(selector='input[type="submit"]', timeout=self.timeout)

            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            self.page.wait_for_load_state("domcontentloaded", timeout=self.timeout)
            self.page.wait_for_load_state("load", timeout=self.timeout)

            while True:
                button = self.page.query_selector('#agree_button')
                if button is not None:
                    button.click()
                    break
            self.name_id = {}
            for x in BeautifulSoup(self.page.query_selector("#_4_1termCourses_noterm > ul").inner_html(),
                                   features="html.parser").find_all("a"):
                start = x.text.find(")") + 1
                end = x.text.find(":")
                if start == -1 or end == -1:
                    continue
                else:
                    get_id = x.get("href")
                    self.name_id[x.text[start:end]] = parse_qs(urlparse(get_id).query).get('id', [None])[0]

    def get_id_subjects(self) -> dict:
        return self.name_id


class LogWebsite:
    def __init__(self, page: Page, user, password, subject, timeForEnd, unvercity="seu"):
        self.page = page
        self.user = password
        self.password = user
        self.unvercity = unvercity
        self.subject = subject
        self.timeout = 99999999

        self.page.goto(
            f"https://lms.seu.edu.sa/webapps/collab-ultra/tool/collabultra/lti/launch?course_id={self.subject}",
            timeout=self.timeout)
        self.page.wait_for_load_state("networkidle", timeout=self.timeout)
        self.page.wait_for_load_state("domcontentloaded", timeout=self.timeout)
        self.page.wait_for_load_state("load", timeout=self.timeout)

        self.page.click('div[class="item-list__item-details"]')

        self.page.wait_for_load_state("networkidle", timeout=self.timeout)
        self.page.wait_for_load_state("domcontentloaded", timeout=self.timeout)
        self.page.wait_for_load_state("load", timeout=self.timeout)

        self.page.click(".launch-button > button:nth-child(1)")

        self.page.wait_for_load_state("networkidle", timeout=self.timeout)
        self.page.wait_for_load_state("domcontentloaded", timeout=self.timeout)
        self.page.wait_for_load_state("load", timeout=self.timeout)

        sleep(3600)#int(timeForEnd))
