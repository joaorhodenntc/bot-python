const puppeteer = require('puppeteer');
const TelegramBot = require('node-telegram-bot-api');
const os = require('os');
const readline = require('readline');

const token = '7346261146:AAERS6EyX2kU4ATsJ0IVZPwy2or65i5uwDE';
const chat_bot = '-1002235800968';
const bot = new TelegramBot(token, { polling: true });

let lastMainMessageId = null;
let greensConsecutivos = 0;
let greensSG = 0;
let greensG1 = 0;
let greensG2 = 0;
let reds = 0;

async function enviarMensagemTelegram(chat_id, mensagem, replyToMessageId = null) {
  try {
    const response = await bot.sendMessage(chat_id, mensagem, {
      parse_mode: 'Markdown',
      disable_web_page_preview: true,
      reply_to_message_id: replyToMessageId 
    });
    return response.message_id;
  } catch (error) {
    console.error('Erro ao enviar mensagem para o Telegram:', error);
  }
}

bot.onText(/\/start/, () => {
  bot.sendMessage(1905184571, `🚀 *Placar do dia:* 🟢 ${greensSG+greensG1+greensG2}  🔴 ${reds}\n\n🎯  SG ${greensSG} | G1 ${greensG1} | G2 ${greensG2}\n\n💰 *Estamos com ${greensConsecutivos} Greens seguidos!*`, { parse_mode: 'Markdown' });
});

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
        '--no-sandbox',
    ],
  });
  const page = await browser.newPage();
  
  await page.goto('https://www.tipminer.com/historico/playpix/aviator?limit=1&t=1724540814597&subject=filter');

  let lastTime = '';
  let menores_consecutivos = 0
  let maiores_consecutivos = 0
  let g1 = "";
  let g2 = "";
  const qtdRepeticoes = 2;

  const checkForUpdates = async () => {

    await page.waitForSelector('.grid__row.flex.flex-1.flex-row.items-start.justify-between');

    const data = await page.evaluate(() => {
      const gridRow = document.querySelector('.grid__row.flex.flex-1.flex-row.items-start.justify-between');
      
      const lastGroup = gridRow.querySelectorAll('.group.relative');
      const lastGroupElement = lastGroup[lastGroup.length - 1];
      
      // Captura o último valor
      const cellResult = lastGroupElement.querySelector('.cell__result').innerText;
      
      // Captura o horário
      const cellDate = lastGroupElement.querySelector('.cell__date').innerText;

      return { result: cellResult, time: cellDate };
    });

    if (data && data.time !== lastTime) {
      lastTime = data.time;

      ultimo_numero_str = data.result.replace('x', '').replace(',', '.');
      ultimo_numero = parseFloat(ultimo_numero_str);
      console.log(ultimo_numero_str);

      if(ultimo_numero < 2.00){
        menores_consecutivos++;
        maiores_consecutivos = 0;
      }

      if(ultimo_numero>=2.00){
        if(menores_consecutivos == qtdRepeticoes){
            await enviarMensagemTelegram(chat_bot, `GREEN SG (${ultimo_numero}) ✅`, lastMainMessageId);
            greensSG++;
            greensConsecutivos++;
        }
        if(menores_consecutivos == qtdRepeticoes+1){
            await enviarMensagemTelegram(chat_bot, `GREEN G1 (${g1}) | (${ultimo_numero}) ✅`, lastMainMessageId);
            greensG1++;
            greensConsecutivos++;
        }
        if(menores_consecutivos == qtdRepeticoes+2){
            await enviarMensagemTelegram(chat_bot, `GREEN G2 (${g1}) | (${g2}) | (${ultimo_numero}) ✅`, lastMainMessageId);
            greensG2++;
            greensConsecutivos++;
        }
        maiores_consecutivos++;
        menores_consecutivos = 0;
      }

      if (menores_consecutivos == qtdRepeticoes){
        lastMainMessageId = await enviarMensagemTelegram(chat_bot, `Realizar entrada após ${ultimo_numero_str}`);
      }

      if(menores_consecutivos == qtdRepeticoes+1){
        g1 = ultimo_numero;
      }

      if(menores_consecutivos == qtdRepeticoes+2){
        g2 = ultimo_numero;
      }

      if(menores_consecutivos == qtdRepeticoes+3){
        await enviarMensagemTelegram(chat_bot, `RED (${g1}) | (${g2}) | (${ultimo_numero}) 🔻`, lastMainMessageId);
        reds++;
        greensConsecutivos = 0;
      }
    }

  };

  const monitorSystemUsage = () => {
    const totalMemory = os.totalmem();
    const freeMemory = os.freemem();
    const usedMemory = totalMemory - freeMemory;
    const memoryUsagePercent = (usedMemory / totalMemory) * 100;

    const cpus = os.cpus();
    const idle = cpus.reduce((acc, cpu) => acc + cpu.times.idle, 0);
    const total = cpus.reduce((acc, cpu) => acc + Object.values(cpu.times).reduce((a, b) => a + b, 0), 0);
    const cpuUsagePercent = 100 - (idle / total) * 100;

    console.log(`Uso de CPU: ${cpuUsagePercent.toFixed(2)}%`);
    console.log(`Uso de Memoria: ${memoryUsagePercent.toFixed(2)}%`);
  };

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.on('line', (input) => {
    if (input.trim() === 'status') {
      monitorSystemUsage();
    }
  });

  setInterval(checkForUpdates, 1000);

})();