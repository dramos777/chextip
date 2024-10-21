#!/usr/bin/env python


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time


def intelbras_gkm2210t():
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://HTTP_USER:HTTP_PASSWORD@CURRENTATAIP")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located(("id", "linkMenu7"))
        )

        reboot_menu = firefox.find_element("id", "linkMenu7")
        reboot_menu.click()

        time.sleep(5)

        reboot_button = firefox.find_element(By.XPATH, "//input[@value=' Reiniciar ' and @class='botaoGeral']")
        reboot_button.click()

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        firefox.quit()


def intelbras_ata200():
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://CURRENTATAIP")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located(("name", "username"))
        )

        username = firefox.find_element("name", "username")
        username.send_keys("HTTP_USER")

        password = firefox.find_element("name", "password")
        password.send_keys("HTTP_PASSWORD")

        login_button = firefox.find_element("id", "login_button")
        login_button.click()

        time.sleep(5)

        firefox.switch_to.frame("menuFrame")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located(("id", "strTools"))
        )

        tools_menu = firefox.find_element("id", "strTools")
        tools_menu.click()
        reboot_menu = firefox.find_element("id", "strDeviceRestart")
        reboot_menu.click()

        firefox.switch_to.default_content()

        time.sleep(5)

        firefox.switch_to.frame("mainframe")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located(("id", "strReboot"))
        )

        reboot_button = firefox.find_element("id", "strReboot")
        reboot_button.click()

        time.sleep(5)

        alert = firefox.switch_to.alert
        alert.accept()

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        firefox.quit()

def khomp():
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://CURRENTATAIP")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located(("name", "pass"))
        )

        password = firefox.find_element("name", "pass")
        password.send_keys("HTTP_PASSWORD")
        password.send_keys(Keys.ENTER)

        time.sleep(5)

        firefox.switch_to.default_content()
        firefox.switch_to.frame("menuFrame")

        restart_button = firefox.find_element(By.XPATH, '//input[@value="REINICIAR" and @style="width:100%"]')
        time.sleep(5)
        restart_button.click()

        time.sleep(5)

        alert = firefox.switch_to.alert
        alert.accept()

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        firefox.quit()

# Call your functions
PYTHON_COMMAND()
