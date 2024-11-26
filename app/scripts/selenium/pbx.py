#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains


# PBX public IP fix
def pbx_ip_fix():
    try:
        option = Options()
        option.add_argument('--headless')
        firefox = webdriver.Firefox(options=option)
        firefox.get("https://SIPURL")

        # Login na interface
        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="userid"]'))
        )
        username = firefox.find_element(By.XPATH, '//*[@id="userid"]')
        username.send_keys("PBXUSER")

        password = firefox.find_element(By.XPATH, '//*[@id="userpass"]')
        password.send_keys("PBXPASSWORD")
        password.send_keys(Keys.RETURN)

        # Navegar até o menu de administrador
        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div/div/ul/li[4]/a'))
        )
        admin_button = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div/div/ul/li[4]/a')
        admin_button.click()

        # Acessar o menu do firewall
        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/ul/li/a'))
        )
        firewall_button = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/ul/li/a')
        firewall_button.click()

        # Acessar a lista de configuração
        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/ul/li/ul/li/a'))
        )
        config_button = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/ul/li/ul/li/a')
        config_button.click()

        # Abrir a lista de acesso
        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div/div[1]/form/div[2]/ul/li[3]/a'))
        ).click()
        access_list = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div/div[1]/form/div[2]/ul/li[3]/a')
        access_list.click()

        # Obter todas as linhas que contêm os campos whitelist
        rows = firefox.find_elements(By.XPATH, '//tr[td/input[starts-with(@id, "whitelist")]]')

        # IP da RB e descrição atual no PBX
        new_ip = "RB_PUB_IP"
        rb_description = "COND_DESCRIPTION"

        # Se o IP cadastrado no PBX for diferente do IP da RB atualizar
        for row in rows:
            # Localizar os campos 'description' e 'host' na mesma linha
            description_field = row.find_element(By.XPATH, './/input[starts-with(@id, "whitelist") and contains(@id, "[description]")]')
            host_field = row.find_element(By.XPATH, './/input[starts-with(@id, "whitelist") and contains(@id, "[host]")]')

            # Obter os valores dos campos
            description = description_field.get_dom_attribute("value")
            host = host_field.get_dom_attribute("value")

            # Verificar se o IP é o desejado
            if host != new_ip and description == rb_description:
                # print(f"IP encontrado na linha com descrição: {description}")
            
                # Alterar o valor do IP
                host_field.clear()
                host_field.send_keys(new_ip)
                host_field.send_keys(Keys.RETURN)
                # print(f"IP alterado de {old_ip} para {new_ip}")
                break
        else:
                # Scroll Down until the "Adicionar" button
                element = firefox.find_element(By.CSS_SELECTOR, "span.repeat-add")
                firefox.execute_script("arguments[0].scrollIntoView();", element)
                element.click()

                # Localizar todas as linhas da tabela
                rows = WebDriverWait(firefox, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//tr[td/input[starts-with(@id, "whitelist")]]'))
                )

                if rows:
                    last_row = rows[-1]  # Acessar a última linha
#                    print("Última linha encontrada!")

                    # Localizar os campos dentro da última linha
                    description_field = last_row.find_element(By.XPATH, './/input[contains(@id, "[description]")]')
                    host_field = last_row.find_element(By.XPATH, './/input[contains(@id, "[host]")]')

                    # Alterar os valores dos campos
                    new_description = "COND_DESCRIPTION"
                    new_host = "RB_PUB_IP"

                    description_field.clear()
                    description_field.send_keys(new_description)

                    host_field.clear()
                    host_field.send_keys(new_host)
                    host_field.send_keys(Keys.RETURN)
#                    print(f"Descrição alterada para '{new_description}' e IP para '{new_host}'.")


        # Remover IP da blocklist
        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div/div[1]/form/div[2]/ul/li[4]/a'))
        )
        block_list = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div/div[1]/form/div[2]/ul/li[4]/a')
        firefox.execute_script("arguments[0].click();", block_list)


        WebDriverWait(firefox, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="firewall-banlist"]'))
        )

	#Find line with content needed
        rows = firefox.find_elements(By.XPATH, '//*[@id="firewall-banlist"]//tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if cells and cells[0].text == new_ip:

                button = row.find_element(By.CLASS_NAME, 'fa-trash')
                button.click()
                break

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        firefox.quit()

# Chama a função
if __name__ == "__main__":
    pbx_ip_fix()

