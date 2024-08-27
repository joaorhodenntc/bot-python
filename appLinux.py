from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import re

TOKEN = '7346261146:AAERS6EyX2kU4ATsJ0IVZPwy2or65i5uwDE'
chat_id = '-1002235800968'
bot = Bot(token=TOKEN)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

service = Service("/usr/local/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://www.tipminer.com/historico/playpix/aviator?limit=1&t=1724540814597&subject=filter')

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


lastMainMessageId  = None
ultimo_horario = None
menores_consecutivos = 0
maiores_consecutivos = 0
greensConsecutivos = 0
greensSG = 0
greensG1 = 0
greensG2 = 0
reds = 0
g1 = 0
g2 = 0
qtdRepeticoes = 2

async def main():
    global ultimo_horario, menores_consecutivos, maiores_consecutivos, greensConsecutivos, lastMainMessageId, greensSG, greensG1, greensG2, reds, g1, g2, qtdRepeticoes

    while True:
        try:
            # Espera até o elemento estar presente
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.grid__row.flex.flex-1.flex-row.items-start.justify-between'))
            )

            grid_row = driver.find_element(By.CSS_SELECTOR, '.grid__row.flex.flex-1.flex-row.items-start.justify-between')
            cell_result = grid_row.find_element(By.CSS_SELECTOR, '.cell__result').text
            cell_date = grid_row.find_element(By.CSS_SELECTOR, '.cell__date').text

            if cell_date != ultimo_horario:
                
                ultimo_numero_str = re.sub(r'x$', '', cell_result).replace(',', '.')
                ultimo_numero = float(ultimo_numero_str)
                ultimo_horario = cell_date
                print(f"Resultado: {cell_result}")

                if ultimo_numero < 2.00:
                    menores_consecutivos += 1
                    maiores_consecutivos = 0

                if ultimo_numero >= 2.00:
                    if menores_consecutivos == qtdRepeticoes:
                        await enviar_mensagem_telegram(chat_id, f"GREEN SG ({ultimo_numero}) ✅", lastMainMessageId)
                        greensSG += 1
                        greensConsecutivos +=1 

                    if menores_consecutivos == qtdRepeticoes+1:
                        await enviar_mensagem_telegram(chat_id, f"GREEN G1 ({g1}) | ({ultimo_numero}) ✅", lastMainMessageId)            
                        greensG1 += 1
                        greensConsecutivos +=1  

                    if menores_consecutivos == qtdRepeticoes+2:
                        await enviar_mensagem_telegram(chat_id, f"GREEN G2 ({g1}) | ({g2}) | ({ultimo_numero}) ✅", lastMainMessageId)
                        greensG2 += 1
                        greensConsecutivos +=1

                    maiores_consecutivos += 1
                    menores_consecutivos = 0

                if menores_consecutivos == qtdRepeticoes:
                    lastMainMessageId = await enviar_mensagem_telegram(chat_id, f"Realizar entrada após o {ultimo_numero}")

                if menores_consecutivos == qtdRepeticoes+1:
                    g1 = ultimo_numero

                if menores_consecutivos == qtdRepeticoes+2:
                     g2 = ultimo_numero

                if menores_consecutivos == qtdRepeticoes+3:
                    await enviar_mensagem_telegram(chat_id, f"RED ({g1}) | ({g2}) | ({ultimo_numero})🔻", lastMainMessageId)
                    reds += 1
                    greensConsecutivos = 0
                    
        except Exception as e:
            print(f"Erro ao acessar os dados: {e}")

        # Aguarda 1 segundo antes de verificar novamente
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
