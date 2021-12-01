import time

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


class Crawler:
    def __init__(self, url: str):
        self.driver = Firefox(service=Service(GeckoDriverManager().install()))
        self.driver.get(url)
        if self.driver.find_elements(By.CLASS_NAME, "captcha"):
            self.solveCaptcha()

    def close(self):
        self.driver.close()

    def getName(self):
        for tag in self.driver.find_elements(By.CLASS_NAME, "main-title"):
            if tag.text == 'Név/Name:':
                return tag.find_element(By.XPATH, "following-sibling::*").text

    def getValidity(self):
        for tag in self.driver.find_elements(By.CLASS_NAME, "valid-card"):
            if tag.text == 'érvényes/valid':
                return True
        return False

    def solveCaptcha(self):
        while self.driver.find_elements(By.CLASS_NAME, "captcha"):
            time.sleep(1)


if __name__ == '__main__':
    c = Crawler(
        "https://www.eeszt.gov.hu/covid-card/-/az/eyJhbGciOiJIUzI1NiJ9"
        ".eyJpc3MiOiJFRVNaVCIsInN1YiI6IjI0MjEwMjc5MTAzMTgzMTQ3Ny4xIiwiaWQiOjU2MjE0MjY1MzB9.iv5BOcKCev6z8olFjcWRkY-b96"
        "-ex_aQXKLWpO8M0kQ")
    print(c.getName())
    print(c.getValidity())
    c.close()
