from datetime import datetime

from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright

import send_log


class Get:
    def __init__(self, page: Page, user_name: str = None, password: str = None):
        self.user = user_name
        self.password = password
        self.user = "S200179212"
        self.password = "Dd4762002"
        self.timeout = 99999999

        page.goto(url="https://bannservices.seu.edu.sa/ssomanager/c/SSB?pkg=bwskfshd.P_CrseSchdDetl",
                  timeout=self.timeout, wait_until="load")
        page.fill(selector='input[id="username"]', value=self.user)
        page.fill(selector='input[id="password"]', value=self.password)
        page.click(selector='button[type="submit"]')

        page.wait_for_load_state("networkidle", timeout=self.timeout)
        page.wait_for_load_state("domcontentloaded", timeout=self.timeout)
        page.wait_for_load_state("load", timeout=self.timeout)

        try:
            page.click(selector='button[type="submit"]')
        except:
            pass

        page.wait_for_load_state("networkidle", timeout=self.timeout)
        page.wait_for_load_state("domcontentloaded", timeout=self.timeout)
        page.wait_for_load_state("load", timeout=self.timeout)

        check = page.locator(selector='[class="datadisplaytable"] caption')
        table = page.locator(selector='[class="datadisplaytable"] tbody')

        i = 0
        self.sub_data = {}
        while i < check.count():
            data = []
            if check.nth(i).inner_text() == "Scheduled Meeting Times":
                soup = BeautifulSoup(table.nth(i).inner_html(), 'html.parser')
                sub = {}
                table_rows = soup.find_all('tr')
                table_headers = [th.get_text() for th in table_rows[0].find_all('th')]
                for row in table_rows[1:]:
                    row_data = {}
                    row_cells = row.find_all('td')
                    for index, cell in enumerate(row_cells):
                        row_data[table_headers[index]] = cell.get_text()
                    if row_data['Type'] == "Mid Exam" or row_data['Type'] == "Final Exam":
                        continue
                    data.append(row_data)

                self.sub_data[check.nth(i - 1).inner_text()] = data
            i += 1
        page.close()

    def get_schedule(self):
        send_log.Login("getSchedule")
        return self.sub_data


def ReturnNone():
    return None


class GetClasses:
    def __init__(self, data):
        self.result=None
        today = datetime.now().date()
        current_time = datetime.now().time()
        today_name = datetime.now().strftime('%A')
        today_name = today_name[:2] if today_name.startswith("T") else today_name[:1]

        for course, class_list in data.items():
            for class_info in class_list:
                start_date, end_date = map(lambda x: datetime.strptime(x.strip(), '%d/%m/%Y'),
                                           class_info['Date Range'].split(' - '))
                if start_date.date() <= today <= end_date.date() and class_info['Days'] == today_name:
                    start_time, end_time = map(lambda x: datetime.strptime(x.strip(), '%I:%M %p').time(),
                                               class_info['Time'].split(' - '))
                    if start_time <= current_time <= end_time:

                        time1 = datetime.combine(today, start_time)
                        time2 = datetime.combine(today, end_time)
                        time_diff = time2 - time1
                        seconds_diff = time_diff.total_seconds()

                        self.result = course[course.find("-") + 1:course.rfind("-")].strip().replace(" ",
                                                                                                     "-"), seconds_diff
                        send_log.Login("timeStart")

                    else:
                        ReturnNone()

    def DictTime(self):
        return self.result
