#!/usr/bin/env python


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time


def intelbras_gkm2210t():
    firefox = None
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
        if firefox:
            firefox.quit()

def intelbras_ata200():
    firefox = None
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
        if firefox:
            firefox.quit()

def khomp():
    firefox = None
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
        if firefox:
            firefox.quit()

#Intelbras SS3530 is a face device
def intelbras_ss3530():
    firefox = None
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://CURRENTATAIP")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input'))
        )

        username = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input')
        username.send_keys("HTTP_USER")

        password = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/div/input')
        password.send_keys("HTTP_SS3530_PASS")
        password.send_keys(Keys.RETURN)

        time.sleep(5)

        maintenance = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/ul/li[11]')
        maintenance.click()

        reboot_button = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/button/span')
        reboot_button.click()

        time.sleep(5)

        alert = firefox.switch_to.active_element
        alert.send_keys(Keys.RETURN)

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        if firefox:
            firefox.quit()

#Intelbras SS3532 is a face device
def intelbras_ss3532():
    firefox = None
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://CURRENTATAIP")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input'))
        )

        username = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input')
        username.send_keys("HTTP_USER")

        password = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/div/input')
        password.send_keys("HTTP_SS3532_PASS")
        password.send_keys(Keys.RETURN)

        time.sleep(7)

        WebDriverWait(firefox, 15).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/div/div/ul/li[15]'))
        )

        time.sleep(7)

        maintenance = firefox.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/div/div/ul/li[15]')
        maintenance.click()

        reboot_button = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/button/span')
        reboot_button.click()

        time.sleep(5)

        alert = firefox.switch_to.active_element
        alert.send_keys(Keys.RETURN)

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        if firefox:
            firefox.quit()

#Intelbras XPE-3200-IP-FACE
def intelbras_xpe3200():
    firefox = None
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://CURRENTATAIP")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]'))
        )

        username = firefox.find_element(By.XPATH, '//*[@id="username"]')
        username.send_keys("HTTP_USER")

        password = firefox.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys("HTTP_XPE3200_PASS")
        password.send_keys(Keys.RETURN)

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="tMenu60"]'))
        )

        update_button = firefox.find_element(By.XPATH, '//*[@id="tMenu60"]')
        firefox.execute_script("arguments[0].scrollIntoView(true);", update_button)
        time.sleep(5)

        update_button.click()

        reboot_button = firefox.find_element(By.XPATH, '//*[@id="Reboot"]')
        reboot_button.click()

        alert = firefox.switch_to.alert
        alert.accept()

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        if firefox:
            firefox.quit()

# Call your functions
PYTHON_COMMAND()
