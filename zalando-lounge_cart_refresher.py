"""Script to refresh item reservation in Zalando lounge

Once an item is added to cart in Zalando lounge this item will be reserved for
a period of 20 minutes. 5 minutes before the end of your reservation or
later, pop-up should appear asking if you want to extend your reservation. The
sole purpose of this script is to wait for this popup to appear and then
click button which will refresh reservation time to another 20 minutes.

In order for this script to work you must have Firefox browser with a profile
in which you are already logged into your zalando account. The path to
directory containing this profile should be given as a command line argument.
For example dir path in Ubuntu may look like this:
"/home/user/.mozilla/firefox/abc123x3.default-release"

Script will run indefinitely until interrupted
"""

import random
import sys
import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

WAIT_TIME = 1800  # 30min because why not?


def refresh(driver: webdriver) -> None:
    while True:
        try:
            # The button we are interested in has nested <span> tag that has id
            # attribute, so it would be easier to just get parent of this
            # <span> tag, but as it turns out, this id is automatically
            # generated probably by whatever framework Zalando is using,
            # so we can't depend on it. But button that we want to grab
            # has sibling <a> tag with href attribute that never changes. So
            # we grab that <a> tag by its href attribute, then that tag's
            # parent, and finally our button.
            btn = WebDriverWait(driver, WAIT_TIME).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//a[contains(@href, "/checkout/")]/../button')))
            time.sleep(random.randint(3, 10))  # Just to not click too fast
            btn.click()
        except TimeoutException:
            pass


def main() -> None:
    if len(sys.argv) > 1:
        options = Options()
        options.add_argument("-profile")
        options.add_argument(sys.argv[1])
        driver = webdriver.Firefox(options=options)
        driver.get("https://www.zalando-lounge.pl")
        refresh(driver)
    else:
        print("You need to specify path to Firefox profile directory as an "
              "argument.")


if __name__ == '__main__':
    main()
