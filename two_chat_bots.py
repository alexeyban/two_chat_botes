"""
Modified MIT License

Software Copyright (c) 2019 OpenAI

We don’t claim ownership of the content you create with GPT-2, so it is yours to do with as you please.
We only ask that you use GPT-2 responsibly and clearly indicate your content was created using GPT-2.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.
The above copyright notice and this permission notice need not be included
with content created by the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

"""

import asyncio
import aiohttp  # Добавлен импорт aiohttp
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Токены ботов от BotFather
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Получите на deepseek.com
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
TOKEN_BOT2 = os.getenv("TELEGRAM_TOKEN_3")

TOKEN_BOT1 = os.getenv("TELEGRAM_TOKEN_1")


# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('telegram.ext').setLevel(logging.DEBUG)  # Детализированные логи от telegram.ext
logger = logging.getLogger(__name__)

time_to_wait_to_answaer = 10 # seconds

# Глобальная переменная для chat_id группы
CHAT_ID = None  # Замените на ID вашей группы после первого запуска


# Функция для получения ответа от DeepSeek
async def get_deepseek_response(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.7
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(DEEPSEEK_API_URL, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    logger.error(f"Ошибка DeepSeek API: {response.status} - {await response.text()}")
                    return "Извини, не могу ответить сейчас!"
        except Exception as e:
            logger.error(f"Исключение при запросе к DeepSeek: {e}")
            return "Что-то пошло не так!"


# Функция для непрерывного диалога
async def run_conversation(app1, app2):
    logger.info(f"Начинаем непрерывный диалог в чате {CHAT_ID}")
    last_message = "Привет, Bot2! Как дела?"  # Начальное сообщение от Bot1
    turn = 1  # Чётко чередуем: 1 - Bot1, 2 - Bot2

    while True:
        try:
            if turn == 1:
                # Bot1 отправляет сообщение

                prompt = f"Bot2 сказал: '{last_message}'. Ответь как Bot1 на русском языке. ты всячески над ним шутишь над оппонентом вспоминая последние мировые события и споришь. ты провоцируешь оппонента на конфликт. отвечай кратко. до 100 слов, можно использовать русскую бранную лексику. исключи шутки про ИИ и украину"
                last_message = await get_deepseek_response(prompt)

                await app1.bot.send_message(chat_id=CHAT_ID, text=last_message)
                logger.info(f"Bot1: {last_message}")
                turn = 2  # Переключаем на Bot2
            elif turn == 2:
                # Bot2 отвечает через DeepSeek
                prompt = f"Bot1 сказал: '{last_message}'. Ответь как Bot2 на русском языке. ты всячески над ним шутишь над оппонентом вспоминая последние мировые события и споришь. ты провоцируешь оппонента на конфликт. отвечай кратко. до 100 слов, можно использовать русскую бранную лексику. исключи шутки про ИИ и украину"
                last_message = await get_deepseek_response(prompt)
                await app2.bot.send_message(chat_id=CHAT_ID, text=last_message)
                logger.info(f"Bot2: {last_message}")
                turn = 1  # Переключаем на Bot1

            await asyncio.sleep(time_to_wait_to_answaer)  # Задержка 10 секунд между сообщениями
        except TelegramError as e:
            logger.error(f"Ошибка Telegram: {e}")
            await asyncio.sleep(time_to_wait_to_answaer // 2)  # Пауза перед повторной попыткой


# Основная функция
async def main():
    # Настройка Bot1
    app1 = Application.builder().token(TOKEN_BOT1).build()
    logger.info("Bot1 настроен (@BotForTestingPurposesForAlex_bot)")

    # Настройка Bot2
    app2 = Application.builder().token(TOKEN_BOT2).build()
    logger.info("Bot2 настроен (@alexeys_poker_game_bot)")

    # Инициализация приложений
    await app1.initialize()
    await app2.initialize()
    logger.info("Оба приложения инициализированы")

    # Запуск ботов
    await app1.start()
    await app2.start()
    logger.info("Оба бота запущены")

    # Запуск диалога
    logger.info("Запускаем непрерывный диалог")
    conversation_task = asyncio.create_task(run_conversation(app1, app2))

    # Ожидание завершения
    logger.info("Боты активны. Нажмите Ctrl+C для остановки.")
    try:
        await conversation_task
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки, завершаем работу")
        await app1.stop()
        await app2.stop()


if __name__ == "__main__":
    logger.info("Запуск программы")
    asyncio.run(main())
