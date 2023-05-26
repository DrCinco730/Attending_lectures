from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright


class Get:
    def __init__(self, page: Page, user_name: str = None, password: str = None):
        self.user = user_name
        self.password = password
        self.user = "S200179212"
        self.password = "Dd4762002"
        self.timeout = 99999999

        page.goto(url="https://bannservices.seu.edu.sa/ssomanager/c/SSB?pkg=bwskfshd.P_CrseSchdDetl",
                  timeout=self.timeout)
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

    def get_schedule(self):
        return self.sub_data
