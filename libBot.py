import time

from datetime import datetime as dt, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from flask import Flask, request, render_template

# key:room, value:capacity dropdown value
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


def book(room):
    with open("credentials.txt") as file:
        USR = file.readline()
        PWD = file.readline()

    one_week_ahead = (dt.today() + timedelta(days=5)).strftime("%Y-%m-%d")
    driver = webdriver.Chrome()

    driver.get("https://libcal.usfca.edu/r/accessible?lid=946&gid=1617")

    capacity_box = driver.find_element(By.NAME, "capacity")
    capacity_box.click()

    number_of_people = driver.find_element(By.XPATH, f"//option[@value='{rooms.get(room)}']")
    number_of_people.click()

    room_selection = driver.find_element(By.XPATH, f"//*[text()={room}]")
    room_selection.click()

    submit = driver.find_element(By.CLASS_NAME, "btn-primary")
    submit.click()

    day = driver.find_element(By.NAME, "date")
    day.click()

    wednesday = driver.find_element(By.XPATH, f"//option[@value='{one_week_ahead}']")
    wednesday.click()

    availability = driver.find_element(By.CLASS_NAME, "btn-primary")
    availability.click()

    # 4-5pm
    first_hour = driver.find_element(By.XPATH, f"//input[@data-start='{one_week_ahead} 16:00:00']")
    first_hour.click()

    # 5-6pm
    second_hour = driver.find_element(By.XPATH, f"//input[@data-start='{one_week_ahead} 17:00:00']")
    second_hour.click()

    submit_times = driver.find_element(By.ID, "s-lc-submit-times")
    submit_times.click()
    time.sleep(3)

    usr_login = driver.find_element(By.ID, "username")
    usr_login.send_keys(USR)

    pwd_login = driver.find_element(By.ID, "password")
    pwd_login.send_keys(PWD)
    pwd_login.send_keys(Keys.RETURN)

    final_submit = driver.find_element(By.ID, "btn-form-submit")
    final_submit.click()

# Initialize app
app = Flask(__name__)

# Set home page
@app.route("/", methods=["GET", "POST"])
def reserveRoom():
    return render_template("HomePage.html")

# Set confirmation page landing
@app.route("/confirmation", methods=["GET", "POST"])
def confirmation():
    response = request.form.get("action")
    book(response)

    return render_template("ConfirmationPage.html")

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2050, debug=True)
