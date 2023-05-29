from Student import *
from GetSchedule import *


def run_get_classes():
    result = GetClasses(data=schedule).DictTime()
    if result is not None:
        course, time_between = result
        course = course[course.find("-") + 1:course.rfind("-")].strip().replace(" ", "-")
        print("Class available:", course)
        LogWebsite(page, "S200179212", "Dd4762002", subject=dictionary22[course], timeForEnd=time_between)
    else:
        pass


if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False,
                                   args=["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream"])
        context = browser.new_context(storage_state="us.json")
        page = context.new_page()
        subjects_dict = GetIdSubjects(page, user="S200179212", password="Dd4762002")
        schedule = Get(page).get_schedule()
        print()
        dictionary22 = subjects_dict.get_id_subjects()

        while True:
            run_get_classes()
            sleep(5)
