from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

s = Service("C:\\Development\\chromedriver.exe")


class InternetSpeedTwitterBot:
    def __init__(self, upload, download, provider):
        self.driver = webdriver.Chrome(service=s)
        self.upload = upload
        self.download = download
        self.provider = provider
        self.wait = WebDriverWait(self.driver, 90)
        self.test_upload = None
        self.test_download = None
        self.tweet_statement = None

        self.driver.maximize_window()

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        try:
            start_btn = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "start-text")))
        finally:
            start_btn.click()

        # Tried to avoid the time.sleep but couldn't get selenium to focus on the popup and exit. This was a workaround
        try:
            time.sleep(39)
            pop_up_close_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div["
                                                                                         "3]/div/div/div/div[2]/div["
                                                                                         "3]/div[3]/div/div["
                                                                                         "8]/div/div/div[2]/a")))
        except UnboundLocalError:
            print("Error")
        else:
            pop_up_close_btn.click()

        self.test_download = int(self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[3]/div/div/div/div["
                                                                      "2]/div[3]/div[3]/div/div[3]/div/div/div["
                                                                      "2]/div[1]/div[2]/div/div[2]/span").text.split(".")[0])
        self.test_upload = int(self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[3]/div/div/div/div["
                                                                    "2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div["
                                                                    "1]/div[3]/div/div[2]/span").text.split(".")[0])

    def results_match(self):
        if self.test_download < self.download and self.test_upload < self.upload:
            self.tweet_statement = f"Hey {self.provider}, my download and upload speeds are {self.test_download}/{self.test_upload} Mbps. I pay for {self.download}/{self.upload} Mbps. What's going on?"
            return False
        elif self.download < self.test_download and self.test_upload >= self.upload:
            self.tweet_statement = f"Hey {self.provider}, my download speeds are {self.test_download}Mbps.I pay for {self.download}Mbps. What's going on?"
            return False
        elif self.download >= self.test_download and self.test_upload < self.upload:
            self.tweet_statement = f"Hey {self.provider}, my upload speeds are {self.upload}Mbps. I pay for {self.upload}Mbps up. What's going on?"
            return False
        else:
            return True

    def tweet_at_provider(self, user_name, password):
        self.driver.get("https://twitter.com/")

        sign_in_bt = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div")))
        sign_in_bt.click()

        entry_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.r-30o5oe")))
        entry_field.send_keys(user_name)

        next_btn = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[6]/div/span/span')
        next_btn.click()

        pass_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        pass_field.send_keys(password)

        # Tried locating the login button through css selectors, xpath, but nothing worked. This is a workaround by
        # sending the enter key instead of locating login button and clicking.
        pass_field.send_keys(Keys.RETURN)

        tweet_field_unclicked = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div')))
        tweet_field_unclicked.click()

        tweet_field_clicked = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')))
        tweet_field_clicked.send_keys(self.tweet_statement)

        print(self.tweet_statement)
