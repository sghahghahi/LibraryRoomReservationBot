import time

from datetime import datetime as dt, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from flask import Flask, request, render_template


def book(room):
    TWO32 = 12707
    TWO43 = 0

    if room == "232":
        room = TWO32
        dropdown_selection = 2
    else:
        room = TWO43
        dropdown_selection = 1

    with open("credentials.txt") as file:
        USR = file.readline()
        PWD = file.readline()

    one_week_ahead = (dt.today() + timedelta(days=6)).strftime("%Y-%m-%d")
    driver = webdriver.Chrome()

    driver.get("https://libcal.usfca.edu/r/accessible?lid=946&gid=1617")
    time.sleep(3)

    capacity_box = driver.find_element(By.NAME, "capacity")
    capacity_box.click()

    number_of_people = driver.find_element(By.XPATH, "//option[@value='{}']".format(dropdown_selection))
    # number_of_people.click()
    number_of_people.send_keys(Keys.RETURN)

    # room_selection = driver.find_element(By.XPATH, "//option[@value='{}']".format(room))
    room_selection = driver.find_element(By.XPATH, "//option[@value='{}']".format(room))
    room_selection.click()
    time.sleep(2)

    submit = driver.find_element(By.CLASS_NAME, "btn-primary")
    submit.click()
    time.sleep(3)

    day = driver.find_element(By.NAME, "date")
    day.click()
    time.sleep(1)

    wednesday = driver.find_element(By.XPATH, "//option[@value='{}']".format(one_week_ahead))
    wednesday.click()
    time.sleep(1)

    availability = driver.find_element(By.CLASS_NAME, "btn-primary")
    availability.click()
    time.sleep(1)

    # 4-5pm
    first_hour = driver.find_element(By.XPATH, "//input[@data-start='{} 16:00:00']".format(one_week_ahead))
    first_hour.click()

    # 5-6pm
    second_hour = driver.find_element(By.XPATH, "//input[@data-start='{}' 17:00:00']".format(one_week_ahead))
    second_hour.click()
    time.sleep(1)
    

    submit = driver.find_element(By.CLASS_NAME, "btn-primary")
    submit.click()

    usr_login = driver.find_element(By.XPATH, "//input[@id='username']")
    usr_login.send_keys(USR)

    pwd_login = driver.find_element(By.XPATH, "//input[@id='password']")
    pwd_login.send_keys(PWD)
    time.sleep(3)

    # submit = driver.find_element(By.CLASS_NAME, "btn-primary")
    submit.click()

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
    if response == "232":
        book(response)
    else:
        book(response)

    return render_template("ConfirmationPage.html")

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2050, debug=True)
