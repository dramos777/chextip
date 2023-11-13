#!/usr/bin/env python


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


### Interbras/ATA200
def intelbras_ata200():
    option = Options()
    option.headless = True
    firefox = webdriver.Firefox(options=option)
    firefox.get("URL")

    # Wait for
    WebDriverWait(firefox, 10).until(
    EC.visibility_of_element_located(("name", "username"))
    )

    # Find the user field
    username = firefox.find_element("name", "username")
    username.send_keys("HTTP_USER")

    # Find the password field
    password = firefox.find_element("name", "password")
    password.send_keys("HTTP_PASSWORD")

    # Find the login button and click it
    login_button = firefox.find_element("id", "login_button")
    login_button.click()

    time.sleep(3)

    # Switch to menuFrame and open it (tools and reboot menu)
    firefox.switch_to.frame("menuFrame")

    # Wait for
    WebDriverWait(firefox, 10).until(
    EC.visibility_of_element_located(("id", "strTools"))
    )
    tools_menu = firefox.find_element("id", "strTools")
    tools_menu.click()
    reboot_menu = firefox.find_element("id", "strDeviceRestart")
    reboot_menu.click()

    # Switch to default frame
    firefox.switch_to.default_content()

    time.sleep(3)

    # Switch to mainframe and reboot device
    firefox.switch_to.frame("mainframe")

    # Wait for
    WebDriverWait(firefox, 10).until(
    EC.visibility_of_element_located(("id", "strReboot"))
    )
    reboot_button = firefox.find_element("id", "strReboot")
    reboot_button.click()

    # PopUP - Wait and accept
    time.sleep(7)
    alert = firefox.switch_to.alert
    alert.accept()

    firefox.quit()

### Khomp
def khomp():
    option = Options()
    option.headless = True
    firefox = webdriver.Firefox(options=option)
    firefox.get("URL")

    # Wait for
    WebDriverWait(firefox, 10).until(
    EC.visibility_of_element_located(("name", "pass"))
    )

    # Find the password field
    password = firefox.find_element("name", "pass")
    password.send_keys("HTTP_PASSWORD")
    password.send_keys(Keys.ENTER)

    time.sleep(3)

    # Switch to menuFrame and open it (tools and reboot menu)
    firefox.switch_to.default_content()
    firefox.switch_to.frame("menuFrame")


    restart_button = firefox.find_element(By.XPATH, '//input[@value="REINICIAR" and @style="width:100%"]')
    time.sleep(7)
    restart_button.click()


    # PopUP - Wait and accept
    time.sleep(7)
    alert = firefox.switch_to.alert
    alert.accept()

    firefox.quit()

PYTHON_COMMAND()

