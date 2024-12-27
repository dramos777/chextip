#!/usr/bin/env python

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
import time


def intelbras_gkm2210t():
    firefox = None
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://HTTP_USER:HTTP_PASSWORD@CURRENTDEVICEIP")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located(("id", "linkMenu7"))
        )

        reboot_menu = firefox.find_element("id", "linkMenu7")
        reboot_menu.click()

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@value=' Reiniciar ' and @class='botaoGeral']"))
        )

        reboot_button = firefox.find_element(By.XPATH, "//input[@value=' Reiniciar ' and @class='botaoGeral']")
        reboot_button.click()

    except Exception as e:
        print(f"An exception occurred: {e}")
        sys.exit(1)

    finally:
        if firefox:
            firefox.quit()

def intelbras_ata200():
    firefox = None
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://CURRENTDEVICEIP")

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
        sys.exit(1)

    finally:
        if firefox:
            firefox.quit()

def khomp():
    firefox = None
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://CURRENTDEVICEIP:8085")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located(("name", "pass"))
        )

        password = firefox.find_element("name", "pass")
        password.send_keys("HTTP_PASSWORD")
        password.send_keys(Keys.ENTER)

        time.sleep(5)

        firefox.switch_to.default_content()
        firefox.switch_to.frame("menuFrame")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//input[@value="REINICIAR" and @style="width:100%"]'))
        )

        restart_button = firefox.find_element(By.XPATH, '//input[@value="REINICIAR" and @style="width:100%"]')
        time.sleep(5)
        restart_button.click()

        time.sleep(5)

        alert = firefox.switch_to.alert
        alert.accept()

    except Exception as e:
        print(f"An exception occurred: {e}")
        sys.exit(1)

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
        firefox.get("http://CURRENTDEVICEIP")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input'))
        )

        username = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input')
        username.send_keys("HTTP_USER")

        password = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/div/input')
        password.send_keys("HTTP_SS3530_PASS")
        password.send_keys(Keys.RETURN)

        WebDriverWait(firefox, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/ul/li[11]'))
        )

        maintenance = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/ul/li[11]')
        maintenance.click()

        WebDriverWait(firefox, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/button/span'))
        )

        reboot_button = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/button/span')
        reboot_button.click()

        time.sleep(5)

        alert = firefox.switch_to.active_element
        alert.send_keys(Keys.RETURN)

    except Exception as e:
        print(f"An exception occurred: {e}")
        sys.exit(1)

    finally:
        if firefox:
            firefox.quit()

#Intelbras SS3532 is a face device
def intelbras_ss3532():
    firefox = None
    try:
        # Configuração do navegador
        options = Options()
        options.add_argument('--headless')  # Use modo headless se necessário
        firefox = webdriver.Firefox(options=options)
        firefox.get("http://CURRENTDEVICEIP")

        print("Aguardando campo de usuário...")
        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input'))
        )

        # Inserir credenciais
        username = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input')
        username.send_keys("HTTP_USER")

        password = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/div/input')
        password.send_keys("HTTP_SS3532_PASS")
        password.send_keys(Keys.RETURN)

        print("Aguardando desaparecimento do carregador...")
        WebDriverWait(firefox, 20).until(
            EC.invisibility_of_element((By.CLASS_NAME, 'el-loading-spinner'))
        )

        print("Tentando clicar no menu...")
        retry_click_element(
            driver=firefox,
            xpath='/html/body/div/div[2]/div[2]/div[1]/div/div/ul/li[15]',
            max_retries=5,
            wait_time=5
        )

        print("Aguardando botão de reinício...")
        WebDriverWait(firefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/button/span'))
        )
        
        # Clicar no botão de reinício
        reboot_button = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/button/span')
        reboot_button.click()

        print("Confirmando alerta de reinício...")
        
        time.sleep(5)
        alert = firefox.switch_to.active_element
        alert.send_keys(Keys.RETURN)

        print("Dispositivo reiniciado com sucesso!")

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        sys.exit(1)

    finally:
        if firefox:
            firefox.quit()


def retry_click_element(driver, xpath, max_retries=5, wait_time=5):
    """
    Tenta clicar em um elemento até o número máximo de tentativas.
    """
    for attempt in range(max_retries):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            print(f"Elemento clicado com sucesso na tentativa {attempt + 1}!")
            return
        except WebDriverException as e:
            print(f"Erro ao clicar no elemento: {e}. Tentando novamente em {wait_time} segundos...")
            time.sleep(wait_time)

    raise WebDriverException(f"Não foi possível clicar no elemento após {max_retries} tentativas.")

#Intelbras SS3540 is a face device
def intelbras_ss3540():
    firefox = None
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://CURRENTDEVICEIP")

        WebDriverWait(firefox, 25).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input'))
        )

        username = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input')
        username.send_keys("HTTP_USER")

        password = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/div/input')
        password.send_keys("HTTP_SS3540_PASS")
        password.send_keys(Keys.RETURN)

        WebDriverWait(firefox, 25).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/div/div/ul/li[13]'))
        )

        maintenance = firefox.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/div/div/ul/li[13]')
        maintenance.click()

        WebDriverWait(firefox, 25).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/button/span'))
        )

        reboot_button = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/button/span')
        reboot_button.click()

        time.sleep(5)

        alert = firefox.switch_to.active_element
        alert.send_keys(Keys.RETURN)

    except Exception as e:
        print(f"An exception occurred: {e}")
        sys.exit(1)

    finally:
        if firefox:
            firefox.quit()

#Intelbras SS1530 is a face device
def intelbras_ss1530():
    firefox = None
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://CURRENTDEVICEIP")

        WebDriverWait(firefox, 25).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input'))
        )

        username = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input')
        username.send_keys("HTTP_USER")

        password = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/div/input')
        password.send_keys("HTTP_SS1530_PASS")
        password.send_keys(Keys.RETURN)

        WebDriverWait(firefox, 25).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/div/div/ul/li[12]'))
        )

        maintenance = firefox.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/div/div/ul/li[12]')
        maintenance.click()

        WebDriverWait(firefox, 25).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/button/span'))
        )

        reboot_button = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/button/span')
        reboot_button.click()

        time.sleep(5)

        alert = firefox.switch_to.active_element
        alert.send_keys(Keys.RETURN)

    except Exception as e:
        print(f"An exception occurred: {e}")
        sys.exit(1)

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
        firefox.get("http://CURRENTDEVICEIP")

        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]'))
        )

        username = firefox.find_element(By.XPATH, '//*[@id="username"]')
        username.send_keys("HTTP_USER")

        password = firefox.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys("HTTP_XPE3200_PASS")
        password.send_keys(Keys.RETURN)

        WebDriverWait(firefox, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="tMenu60"]'))
        )

        update_button = firefox.find_element(By.XPATH, '//*[@id="tMenu60"]')
        firefox.execute_script("arguments[0].scrollIntoView(true);", update_button)
        time.sleep(5)

        update_button.click()

        WebDriverWait(firefox, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="Reboot"]'))
        )

        reboot_button = firefox.find_element(By.XPATH, '//*[@id="Reboot"]')
        reboot_button.click()

        alert = firefox.switch_to.alert
        alert.accept()

    except Exception as e:
        print(f"An exception occurred: {e}")
        sys.exit(1)

    finally:
        if firefox:
            firefox.quit()


# Controllers Devices

# Linear Module
def linear_module():
    firefox = None
    try:
        option = Options()
        option.add_argument('--headless')
        
        firefox = webdriver.Firefox(options=option)
        firefox.get("http://LINEAR_USER:LINEAR_PASSWORD@CURRENTDEVICEIP")

        try:
            WebDriverWait(firefox, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div/div/div[1]/a[2]'))
            )
        except Exception:
            firefox.refresh()

            WebDriverWait(firefox, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div/div/div[1]/a[2]'))
            )

        network_button = firefox.find_element(By.XPATH, '/html/body/div/div/div/div/div/div[1]/a[2]')
        network_button.click()

        WebDriverWait(firefox, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="e_dns1"]'))
        )

        servername1 = firefox.find_element(By.XPATH, '//*[@id="e_dns1"]')
        servername1.clear()

        servername1.send_keys("8.8.8.8")

        time.sleep(5)

# Wait until servername1 has finished
#        WebDriverWait(firefox, 5).until(
#            EC.staleness_of(servername1)
#        )

        servername1.send_keys(Keys.RETURN)

        time.sleep(5)

    except Exception as e:
        print(f"An exception occurred: {e}")
        sys.exit(1)

    finally:
        if firefox:
            firefox.quit()

# Nice Module
def nice_module():
    firefox = None
    try:
        option = Options()
        option.add_argument('--headless')

        firefox = webdriver.Firefox(options=option)
        firefox.get("http://NICE_USER:NICE_PASSWORD@CURRENTDEVICEIP")

        try:
            WebDriverWait(firefox, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/ul/li[2]/a'))
            )
        except Exception:
            firefox.refresh()
            WebDriverWait(firefox, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/ul/li[2]/a'))
            )

        network_button = firefox.find_element(By.XPATH, '/html/body/div[2]/ul/li[2]/a')
        network_button.click()

        try:
            WebDriverWait(firefox, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/form/button'))
            )
        except Exception:
            firefox.refresh()
            WebDriverWait(firefox, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/form/button'))
            )

        save_button = firefox.find_element(By.XPATH, '/html/body/div[3]/form/button')
        save_button.click()

# Wait until servername1 has finished
#        WebDriverWait(firefox, 5).until(
#            EC.staleness_of(servername1) 
#        )
        
    except Exception as e:
        print(f"An exception occurred: {e}")
        sys.exit(1)

    finally:
        if firefox:
            firefox.quit()

def controlid_idfacemax():
    firefox = None
    try:
        # Configuração do navegador
        options = Options()
        options.add_argument('--headless')  # Use modo headless se necessário
        firefox = webdriver.Firefox(options=options)
        firefox.get("http://CURRENTDEVICEIP")

       # print("Aguardando campo de usuário...")
        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="input_user"]'))
        )

        # Inserir credenciais
        username = firefox.find_element(By.XPATH, '//*[@id="input_user"]')
        username.send_keys("HTTP_USER")

        password = firefox.find_element(By.XPATH, '//*[@id="input_password"]')
        password.send_keys("HTTP_CONTROLID_IDFACEMAX_PASS")
        password.send_keys(Keys.RETURN)

        #print("Aguardando menu aparecer...")
        WebDriverWait(firefox, 20).until(
            EC.invisibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/ul/li[9]/a'))
        )

        firefox.get("http://CURRENTDEVICEIP/pt_BR/html/configurations.html")

        #print("Aguardando botão de reinício...")
        WebDriverWait(firefox, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnReboot > label:nth-child(2)'))
        )

        # Clicar no botão de reinício
        reboot_button = firefox.find_element(By.CSS_SELECTOR, '#btnReboot > label:nth-child(2)')
        firefox.execute_script("arguments[0].scrollIntoView(true);", reboot_button)
        firefox.execute_script("arguments[0].click();", reboot_button)

        #print("Confirmando alerta de reinício...")
        firefox.switch_to.active_element
        alert = firefox.find_element(By.CSS_SELECTOR, 'button.blue:nth-child(2)')
        firefox.execute_script("arguments[0].click();", alert)

        firefox.switch_to.active_element
        alert = firefox.find_element(By.CSS_SELECTOR, 'div.modal-scrollable:nth-child(24) > div:nth-child(1) > div:nth-child(3) > button:nth-child(2)')
        firefox.execute_script("arguments[0].click();", alert)

        time.sleep(3)

        #print("Dispositivo reiniciado com sucesso!")

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        sys.exit(1)

    finally:
        if firefox:
            firefox.quit()

# Call your functions
PYTHON_COMMAND()
