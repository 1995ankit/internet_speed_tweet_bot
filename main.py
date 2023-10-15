from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import os
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
CHROME_DRIVER_PATH = ChromeDriverManager().install()

PROMISED_DOWN = 300
PROMISED_UP = 200
TWITTER_EMAIL = os.environ.get('twitter_email')
TWITTER_PASSWORD = os.environ.get('pass')

class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(service=Service(driver_path))
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get('https://www.speedtest.net/')
        sleep(5)

        cookies = self.driver.find_element(By.ID, value='onetrust-accept-btn-handler')
        cookies.click()

        go_button = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]')
        go_button.click()
        sleep(40)

        try:
            notification_dismiss = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/div/div[2]/a')
            notification_dismiss.click()
        except:
            pass

        sleep(2)
        down_speed = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')
        download_speed = down_speed.text

        up_speed = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
        upload_speed = up_speed.text

        return download_speed, upload_speed

    def tweet_at_provider(self, down_speed, up_speed):
        self.driver.get('https://twitter.com/login')
        sleep(2)

        user_name = self.driver.find_element(By.XPATH, value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        user_name.send_keys(os.environ.get('twitter_email'))
        user_name.send_keys(Keys.ENTER)
        sleep(3)

        password = self.driver.find_element(By.XPATH, value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/'
                                                            'div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password.send_keys(os.environ.get('pass'))
        password.send_keys(Keys.ENTER)
        sleep(5)
        compose_button = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')
        compose_button.click()
        sleep(3)
        tweet = f"Hey Internet Provider, why is my internet speed {down_speed}down/{up_speed}up mbps when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up mbps?"

        tweet_input = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/'
                                                               'div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/'
                                                               'div/div/div/div/div/div[2]/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
        tweet_input.send_keys(tweet)
        sleep(10)


bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
down_speed, up_speed = bot.get_internet_speed()
bot.tweet_at_provider(down_speed, up_speed)
sleep(10)
