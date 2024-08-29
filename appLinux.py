from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot
from telegram.constants import ParseMode
import asyncio
import re
import psutil

TOKEN = '7346261146:AAERS6EyX2kU4ATsJ0IVZPwy2or65i5uwDE'
chat_id = '-1002235800968'
bot = Bot(token=TOKEN)

last_placar_message_id = None

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


async def enviar_placar_atual():
    global last_placar_message_id

    if last_placar_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=last_placar_message_id)
        except Exception as e:
            print('Erro ao excluir a mensagem anterior do placar:', e)

    mensagem = (
        f"🚀 *Placar do dia:* 🟢 {greensSG + greensG1 + greensG2}  🔴 {reds}\n\n"
        f"💰 *Estamos com {greensConsecutivos} Greens seguidos!*"
    )
    

    last_placar_message_id = await enviar_mensagem_telegram(chat_id, mensagem)


def monitor_resources():
    # Monitorar o uso de CPU e memória
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    print(f"CPU: {cpu_usage}% | Memoria: {memory_info.percent}%")


lastMainMessageId  = None
lastAvisoMessageId = None
ultimo_horario = None
menores_consecutivos = 0
maiores_consecutivos = 0
greensConsecutivos = 0
greensSG = 0
greensG1 = 0
greensG2 = 0
greensG3 = 0
greensG4 = 0
greensG5 = 0
reds = 0
g1 = 0
g2 = 0
g3 = 0
g4 = 0
g5 = 0
qtdRepeticoes = 2

async def main():
    global ultimo_horario, menores_consecutivos, maiores_consecutivos, greensConsecutivos, lastMainMessageId, lastAvisoMessageId, greensSG, greensG1, greensG2, greensG3, greensG4, greensG5, reds, g1, g2, g3, g4, g5, qtdRepeticoes

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
                print(f"\nResultado: {cell_result}")

                if lastAvisoMessageId:
                    await bot.delete_message(chat_id=chat_id, message_id=lastAvisoMessageId)
                    lastAvisoMessageId = None

                if ultimo_numero < 2.00:
                    menores_consecutivos += 1
                    maiores_consecutivos = 0

                if ultimo_numero >= 2.00:
                    if menores_consecutivos == qtdRepeticoes:
                        await enviar_mensagem_telegram(chat_id, f"GREEN SG ({ultimo_numero}) ✅", lastMainMessageId)
                        greensSG += 1
                        greensConsecutivos +=1 
                        await enviar_placar_atual()

                    if menores_consecutivos == qtdRepeticoes+1:
                        await enviar_mensagem_telegram(chat_id, f"GREEN G1 ({g1}) | ({ultimo_numero}) ✅", lastMainMessageId)            
                        greensG1 += 1
                        greensConsecutivos +=1  
                        await enviar_placar_atual()

                    if menores_consecutivos == qtdRepeticoes+2:
                        await enviar_mensagem_telegram(chat_id, f"GREEN G2 ({g1}) | ({g2}) | ({ultimo_numero}) ✅", lastMainMessageId)
                        greensG2 += 1
                        greensConsecutivos +=1
                        await enviar_placar_atual()

                    if menores_consecutivos == qtdRepeticoes+3:
                        await enviar_mensagem_telegram(chat_id, f"GREEN G3 ({g1}) | ({g2}) | ({g3}) | ({ultimo_numero}) ✅", lastMainMessageId)
                        greensG3 += 1
                        greensConsecutivos +=1
                        await enviar_placar_atual()

                    if menores_consecutivos == qtdRepeticoes+4:
                        await enviar_mensagem_telegram(chat_id, f"GREEN G4 ({g1}) | ({g2}) | ({g3}) | ({g4}) | ({ultimo_numero}) ✅", lastMainMessageId)
                        greensG4 += 1
                        greensConsecutivos +=1
                        await enviar_placar_atual()

                    if menores_consecutivos == qtdRepeticoes+5:
                        await enviar_mensagem_telegram(chat_id, f"GREEN G5 ({g1}) | ({g2}) | ({g3}) | ({g4}) | ({g5}) |({ultimo_numero}) ✅", lastMainMessageId)
                        greensG5 += 1
                        greensConsecutivos +=1
                        await enviar_placar_atual()

                    maiores_consecutivos += 1
                    menores_consecutivos = 0

                if menores_consecutivos == qtdRepeticoes-1:
                    lastAvisoMessageId = await enviar_mensagem_telegram(chat_id, f"Atentos! Possível entrada 🚨")

                if menores_consecutivos == qtdRepeticoes:
                    lastMainMessageId = await enviar_mensagem_telegram(chat_id, f"🚀 *ENTRADA CONFIRMADA!*\n\n" f"👉 Entrar após: *{cell_result}*\n" f"💰 Sair em 2.00x\n" f"♻️ Até 5º Gales\n\n" f"[CLIQUE AQUI PARA JOGAR](https://www.playpix.com/pb/casino/game-view/806666/aviator)")

                if menores_consecutivos == qtdRepeticoes+1:
                    g1 = ultimo_numero

                if menores_consecutivos == qtdRepeticoes+2:
                     g2 = ultimo_numero
                     
                if menores_consecutivos == qtdRepeticoes+3:
                     g3 = ultimo_numero

                if menores_consecutivos == qtdRepeticoes+4:
                     g4 = ultimo_numero

                if menores_consecutivos == qtdRepeticoes+5:
                     g5 = ultimo_numero

                if menores_consecutivos == qtdRepeticoes+6:
                    await enviar_mensagem_telegram(chat_id, f"RED ({g1}) | ({g2}) | ({g3}) | ({g4}) | ({g5}) | ({ultimo_numero})🔻", lastMainMessageId)
                    reds += 1
                    greensConsecutivos = 0

                monitor_resources()

        except Exception as e:
            print(f"Erro ao acessar os dados: {e}")

        # Aguarda 1 segundo antes de verificar novamente
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
