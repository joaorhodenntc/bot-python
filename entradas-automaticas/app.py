from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot
from telegram.constants import ParseMode
import time
import re
import json
import asyncio

TOKEN = '7346261146:AAERS6EyX2kU4ATsJ0IVZPwy2or65i5uwDE'
chat_id = '-1002211720991'
bot = Bot(token=TOKEN)

#service = Service("C:/WebDriver/chromedriver.exe")
service = Service("/usr/local/bin/chromedriver")

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://games.playpix.com/Inner/authorization.php?partnerId=18750115&gameId=806666&language=pb&openType=real&devicetypeid=1&exitURL=https%3A%2F%2Fwww.playpix.com&deposit_url=https%3A%2F%2Fwww.playpix.com%3Fprofile%3Dopen%26account%3Dbalance%26page%3Ddeposit&frameId=gameView&logoSource=%2Flogo.png%3Fv%3D1722323127&token=D53A46BCF73E5787559AC825F49D1665"



async def enviar_mensagem_telegram(chat_id, mensagem, reply_to_message_id=None):
    try:
        response = await bot.send_message(
            chat_id=chat_id,
            text=mensagem,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_to_message_id=reply_to_message_id
        )
        return response.message_id
    except Exception as e:
        print('Erro ao enviar mensagem para o Telegram:', e)

def ler_dados_json():
    try:
        with open('../dados.json', 'r') as file: #caminho para o LINUX
            dados = json.load(file)
            return dados.get("ultimo_numero"), dados.get("ultimo_horario")
    except FileNotFoundError:
        return None, None

def consultar_saldo():
    saldo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[1]/app-header/div/div[2]/div/div[1]/div/span[1]'))).text
    return saldo

def configurar_aposta():

    auto_aposta = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/app-navigation-switcher/div/button[2]'))
    )

    auto_aposta.click()

    auto_saque = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[1]/app-ui-switcher/div/span'))
    )
    
    auto_saque.click()

    input_saque = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[2]/div/app-spinner/div/div[2]/input'))
    )

    driver.execute_script("arguments[0].value = '';", input_saque)
    input_saque.send_keys("2")

def apostar(valor):

    input_valor = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input'))
    )

    driver.execute_script("arguments[0].value = '';", input_valor)
    input_valor.send_keys(valor)

    apostar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button'))
    )

    apostar_button.click()

lastHorario = None
menoresConsecutivos = 0

async def main():
    global lastHorario, menoresConsecutivos
    
    await enviar_mensagem_telegram(chat_id, "Iniciando BOT 🚨...")
    
    try:
        driver.get(url)
        configurar_aposta()

    except Exception as e:
        print("Erro na url:", str(e))
        await enviar_mensagem_telegram(chat_id, str(e))

    while True:
        try:
            try:
                ultimo_numero, ultimo_horario = ler_dados_json()

            except Exception as e:
                print()
            if lastHorario != ultimo_horario: 
                lastHorario = ultimo_horario
                saldo = consultar_saldo()
                print(f"Último Número: {ultimo_numero} | Saldo: {saldo}")
                
          
                if(ultimo_numero < 2.00):                                                                                                                                
                    menoresConsecutivos+=1
                
                if (ultimo_numero >= 2.00):
                    
                    if(menoresConsecutivos == 6):
                        print(f"\nGREEN SG! {ultimo_numero}")
                        await enviar_mensagem_telegram(chat_id, f"*GREEN SG! {ultimo_numero} ✅* Saldo Atual: {saldo}")
                        print(consultar_saldo())

                    if(menoresConsecutivos == 7):
                        print(f"\nGREEN G1! {ultimo_numero}")
                        await enviar_mensagem_telegram(chat_id, f"*GREEN G1! {ultimo_numero} ✅* Saldo Atual: {saldo}")
                        print(consultar_saldo())

                    if(menoresConsecutivos == 8):
                        print(f"\nGREEN G2! {ultimo_numero}")
                        await enviar_mensagem_telegram(chat_id, f"*GREEN G2! {ultimo_numero} ✅* Saldo Atual: {saldo}")
                        print(consultar_saldo())

                    menoresConsecutivos = 0

                if(menoresConsecutivos == 6):
                    print(f"\nRealizando Aposta...")
                    await enviar_mensagem_telegram(chat_id, f"*Realizando Entrada..* Saldo Atual: {saldo}")
                    apostar(1)

                if(menoresConsecutivos == 7):
                    print(f"\nRealizando Gale 1...")
                    await enviar_mensagem_telegram(chat_id, f"*Realizando Gale 1...* Saldo Atual: {saldo}")
                    apostar(1)

                if(menoresConsecutivos == 8):
                    print(f"\nRealizando Gale 2...")
                    await enviar_mensagem_telegram(chat_id, f"*Realizando Gale 2...* Saldo Atual: {saldo}")
                    apostar(2)

                if(menoresConsecutivos == 9):
                    print(f"\nRed 🔻")
                    await enviar_mensagem_telegram(chat_id, f"*Red 🔻*  Saldo Atual: {saldo}")
                
        except Exception as e:
            print("Erro ao tentar obter o resultado:", str(e))
            await enviar_mensagem_telegram(chat_id, str(e))



if __name__ == '__main__':
    asyncio.run(main())
