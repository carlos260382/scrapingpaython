import cv2
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from pdf2image import convert_from_path
from IPython.display import display, Image
import pyautogui
import time

files_pdf = []
files_png = []
urls = []


def run():

    # Obtengo los archivos PDF para convertir a Imagen, los abro y tomo la captura pantalla
    def get_file_pdf():
        directory = os.getcwd()
        global files_pdf
        with os.scandir(path=directory) as itr:
            for file in itr:
                if file.name.split('.')[-1] == "pdf":
                    files_pdf.append(file.name)

        os.system('explorer')
        for file in files_pdf:
            try:
                file_name_png = file.split('.')[0] + ".png"
                os.startfile(
                    ".\\%s" % file)
                time.sleep(3)
                screenshot = pyautogui.screenshot()
                screenshot.save(
                    ".\\%s" % file_name_png)
            except OSError:
                print("Falló")
            else:
                print("Se creo el archivo png")

    get_file_pdf()

    # Encuentro los archivos imagenes y obtengo las URL

    def get_data_web(urls):
        list_heads = []
        list_rows = []
        chromeOptions = Options()
        chromeOptions.headless = True
        for url in urls:
            time.sleep(1)
            driver = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=chromeOptions)
            driver.set_window_size(1200, 1000)
            driver.get(url)
            time.sleep(1)

            table1 = driver.find_element(
                By.XPATH, '//*[@id="ubicacionForm:j_idt10:0:j_idt11:j_idt14_data"]')

            table1 = table1.text.split('\n')

            for row in table1:
                row1 = row.split(':')[0]
                row2 = row.split(':')[1]
                list_heads.append(row1)
                list_rows.append(row2)

            table2 = driver.find_element(
                By.XPATH, '//*[@id="ubicacionForm:j_idt10:1:j_idt11:j_idt14_data"]')

            table2 = table2.text.split('\n')
            for row in table2:
                row1 = row.split(':')[0]
                row2 = row.split(':')[1]
                list_heads.append(row1)
                list_rows.append(row2)

            table3 = driver.find_element(
                By.XPATH, '//*[@id="ubicacionForm:j_idt10:2:j_idt11:j_idt14_data"]')

            table3 = table3.text.split('\n')
            for row in table3:
                row1 = row.split(':')[0]
                row2 = row.split(':')[1]
                list_heads.append(row1)
                list_rows.append(row2)

        df = pd.DataFrame({'Informacion': list_heads, 'datos': list_rows})
        print(df)
        df.to_excel('file.xlsx', index=False, header=False, encoding='utf-8')

    def get_file_png():
        directory = os.getcwd()
        global files_png
        global urls
        with os.scandir(path=directory) as itr:
            for file in itr:
                if file.name.split('.')[-1] == "png":
                    files_png.append(file.name)

        for file in files_png:
            img = cv2.imread(
                ".\\%s" % file)
            for code in decode(img):
                if (code.type == 'QRCODE'):
                    urls.append(code.data.decode('utf-8'))
        # Obtengo las URL de cada archivo png
        print(urls)
        get_data_web(urls)

    get_file_png()


# Ingreso a cada URL para capturar la data (scraping)


if __name__ == '__main__':
    run()
