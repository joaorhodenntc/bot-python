from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

service = Service("/usr/local/bin/chromedriver")  

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://www.tipminer.com/historico/playpix/aviator?limit=1&t=1724540814597&subject=filter')

ultimo_horario = None

while True:
    try:
        # Espera até o elemento estar presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.grid__row.flex.flex-1.flex-row.items-start.justify-between'))
        )

        # Localiza o elemento
        grid_row = driver.find_element(By.CSS_SELECTOR, '.grid__row.flex.flex-1.flex-row.items-start.justify-between')
        cell_result = grid_row.find_element(By.CSS_SELECTOR, '.cell__result').text
        cell_date = grid_row.find_element(By.CSS_SELECTOR, '.cell__date').text

        if cell_date != ultimo_horario:
            print(f"Resultado: {cell_result} | Horário: {cell_date}")
            ultimo_horario = cell_date

    except Exception as e:
        print(f"Erro ao acessar os dados: {e}")

    # Aguarda 1 segundo antes de verificar novamente
    time.sleep(1)
