import os
import logging
from datetime import datetime as dt, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LibraryRoomReservationBot:
    def __init__(
        self,
        room=232
    ) -> None:

        logger = logging.getLogger("LibraryBotLogger")
        logger.setLevel(logging.DEBUG)

        log_dir = os.getenv("LOGS_DIR_PATH")
        log_file = os.getenv("LOGS_FILE_PATH")

        if not log_dir or not log_file:
            raise EnvironmentError("Environment variable(s) incorrect or not properly set.")

        os.makedirs(log_dir, exist_ok=True)

        log_path = os.path.join(log_dir, log_file)

        logger = logging.getLogger("LibraryBotLogger")
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(file_handler)

        rooms = {
            "242": "1",
            "243": "1",

            "108": "2",
            "202": "2",
            "210": "2",
            "211": "2",
            "212": "2",
            "214": "2",
            "215": "2",
            "216": "2",
            "217": "2",
            "218": "2",
            "219": "2",
            "223": "2",
            "224": "2",
            "229": "2",
            "230": "2",
            "232": "2",
            "233": "2",
            "235": "2",
            "237": "2",
            "238": "2",
            "240": "2",
            "G09": "2",
            "G13": "2",
            "G14": "2",

            "314": "3",
            "315": "3",

            "239": "4",
        }

        # Set instance variables
        self.logger = logger
        self.room = room
        self.rooms = rooms
        self.USR = os.getenv("USF_USERNAME")
        self.PWD = os.getenv("USF_PASSWORD")

        if not self.USR or not self.PWD:
            logger.error("Environment variable(s) incorrect or not properly set.\n")
            raise EnvironmentError("Environment variable(s) incorrect or not properly set.")

        logger.info(f"LibraryRoomReservationBot instantiated for room {self.room}")

    def init_driver(self) -> webdriver.Chrome:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")

        return webdriver.Chrome(options=options)

    def book(self, driver: webdriver.Chrome) -> None:
        try:
            driver.get("https://libcal.usfca.edu/r/accessible?lid=946&gid=1617")
            self.logger.info(f"Visiting {driver.title}")

            capacity_box = driver.find_element(By.NAME, "capacity")
            capacity_box.click()

            number_of_people = driver.find_element(By.XPATH, f"//option[@value='{self.rooms[str(self.room)]}']")

            number_of_people.click()

            room_selection = driver.find_element(By.XPATH, f"//*[text()={self.room}]")
            room_selection.click()

            submit = driver.find_element(By.CLASS_NAME, "btn-primary")
            submit.click()

            day = driver.find_element(By.NAME, "date")
            day.click()

            one_week_ahead = (dt.today() + timedelta(days=6)).strftime("%Y-%m-%d")
            self.logger.info(f"Booking for {one_week_ahead}")

            wednesday = driver.find_element(By.XPATH, f"//option[@value='{one_week_ahead}']")
            wednesday.click()
            self.logger.info("Found day")

            availability = driver.find_element(By.CLASS_NAME, "btn-primary")
            availability.click()
            self.logger.info("Found availability")

            # 2-3pm
            first_hour = driver.find_element(By.XPATH, f"//input[@data-start='{one_week_ahead} 14:00:00']")
            first_hour.click()
            self.logger.info("Successfully clicked first hour")

            # 3-4pm
            second_hour = driver.find_element(By.XPATH, f"//input[@data-start='{one_week_ahead} 16:00:00']")
            second_hour.click()
            self.logger.info("Successfully clicked second hour")

            submit_times = driver.find_element(By.ID, "s-lc-submit-times")
            submit_times.click()
            self.logger.info("Successfully advanced to login page")

            wait = WebDriverWait(driver, 3)
            usr_login = wait.until(EC.element_to_be_clickable((By.ID, "username")))
            self.logger.debug(driver.title)
            usr_login.send_keys(str(self.USR))
            self.logger.info("Successfully sent username")

            pwd_login = driver.find_element(By.ID, "password")
            pwd_login.send_keys(str(self.PWD))
            pwd_login.send_keys(Keys.RETURN)
            self.logger.info("Suggessfully sent password")

            final_submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            final_submit.click()

            self.logger.debug(f"Room {self.room} successfully booked.\n")

            driver.quit()

        except Exception as e:
            self.logger.error(f"{e}\n")
            driver.quit()
            raise e

def main() -> None:
    library_bot = LibraryRoomReservationBot()
    driver: webdriver.Chrome = library_bot.init_driver()
    library_bot.book(driver)

if __name__ == "__main__":
    main()
