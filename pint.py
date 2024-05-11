import telebot
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument('--headless') # режим без GUI
options.add_argument('--disable-gpu')  # отключение GUI

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

bot = telebot.TeleBot("6774684167:AAEHdRKPQRKAsB-MnBOn2FAIuZGKtZMjh6g")

@bot.message_handler(commands = ['search_photo'])
def search_photo(message):
    mess = bot.send_message(message.chat.id, "Введите, какие фотокарточки вы хотите найти?")
    bot.register_next_step_handler(mess, search)

def search(message):

    bot.send_message(message.chat.id, "Сейчас найдем...")
    photo = "https://ru.pinterest.com/search/pins/?q=" + message.text + "&rs=typed"
    driver.get(photo)
    sleep(10)
    photos = driver.find_elements(By.CSS_SELECTOR, "[role='listitem'] img")
    for i in range(len(photos)):

        img_url = photos[i].get_attribute('src')
        #bot.send_message(message.chat.id, img_url)

        # Сохранение изображения на компьютере
        img_data = requests.get(img_url).content
        with open(f"image_{i}.jpg", 'wb') as handler:
            handler.write(img_data)
        # Отправка изображения в Телеграмм
        with open(f"image_{i}.jpg", 'rb') as img:
            bot.send_photo(message.chat.id, img)
            sleep(1)  # Пауза между отправкой изображений

        if i == 4:
            break

bot.polling() #для постоянной работы бота