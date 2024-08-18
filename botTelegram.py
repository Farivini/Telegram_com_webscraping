import os
import json
import requests
from time import sleep
from threading import Thread, Lock
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Carregar configurações sensíveis de variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEB_DRIVER_PATH = os.getenv("WEB_DRIVER_PATH")
AUDATEX_USERNAME = os.getenv("AUDATEX_USERNAME")
AUDATEX_PASSWORD = os.getenv("AUDATEX_PASSWORD")

# Configuração inicial
config = {
    "url": f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/",
    "lock": Lock(),
    "url_file": f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/"
}

def del_update(data):
    print(f'Deletando mensagem id {data["update_id"]}')
    with config['lock']:
        requests.post(config['url'] + 'getUpdates', {'offset': data['update_id'] + 1})

def enviando_msg(data, msg):
    with config['lock']:
        requests.post(config['url'] + 'sendMessage', {'chat_id': data['message']['chat']['id'], 'text': str(msg)})

def pega_documento(file_path):
    return requests.get(config['url_file'] + str(file_path)).content

def upload(data, file):
    formatos = {
        'png': {'metodo': 'sendPhoto', 'send': 'photo'},
        'text': {'metodo': 'sendDocument', 'send': 'document'}
    }
    formato = 'text' if '.txt' in file else 'png'
    return requests.post(
        config['url'] + formatos[formato]['metodo'],
        {'chat_id': data['message']['chat']['id']},
        files={formatos[formato]['send']: open(file, 'rb')}
    ).text

def process_message(data):
    if data['message']['text'] == '/start':
        Thread(target=enviando_msg, args=(data, 'Bem vindo ao assistente da Vsveiculos')).start()
        Thread(target=enviando_msg, args=(data, 'Digite apenas a placa, no modelo antigo e sem traços')).start()
    else:
        Thread(target=enviando_msg, args=(data, 'Aguarde')).start()
        drive = webdriver.Chrome(WEB_DRIVER_PATH)
        drive.get("https://login.audatex.com.br/account/login")
        
        usuario = drive.find_element_by_id("UserName")
        usuario.send_keys(AUDATEX_USERNAME)
        
        senha = drive.find_element_by_id("Password")
        senha.send_keys(AUDATEX_PASSWORD)
        senha.send_keys(Keys.RETURN)
        
        sleep(3)
        sinistro = drive.find_element_by_id("lnkSinistro")
        sinistro.click()
        sleep(3)
        
        buscar = drive.find_element_by_id("lnkBuscarOrcamento")
        buscar.click()
        
        placas = data['message']['text']
        placa = drive.find_element_by_id("ctl00_cphBody_txtPlacaBuscaAvancada")
        placa.send_keys(placas)
        placa.send_keys(Keys.RETURN)
        
        sleep(3)
        orcamento = drive.find_element_by_class_name("TableIn")
        orcamento.click()
        
        comRs = drive.find_element_by_link_text("Laudo Av. de Danos").click()
        drive.find_element_by_id("btnVisualizar").click()
        
        guiaLaudo = drive.window_handles
        drive.switch_to.window(guiaLaudo[1])
        drive.fullscreen_window()
        
        drive.get_screenshot_as_file("Laudo.png")
        upload(data, "Laudo.png")
        
        drive.switch_to.window(guiaLaudo[0])
        sleep(2)
        
        drive.find_element_by_id("btnVisualizarImagem").click()
        guias = drive.window_handles
        drive.switch_to.window(guias[2])
        drive.fullscreen_window()
        
        drive.get_screenshot_as_file("carro.png")
        upload(data, 'carro.png')
        
        drive.find_element_by_tag_name("html").send_keys(Keys.PAGE_DOWN)
        drive.get_screenshot_as_file("carro2.png")
        upload(data, 'carro2.png')
        
        drive.find_element_by_tag_name("html").send_keys(Keys.PAGE_DOWN)
        drive.get_screenshot_as_file("carro3.png")
        upload(data, "carro3.png")
        
        enviando_msg(data, "Pronto! Para consultar outra, é só mandar mais uma placa 🏎.")
        drive.quit()

while True:
    try:
        recebe = json.loads(requests.get(config["url"] + "getUpdates").text)
    except Exception as e:
        print("Erro na conexão:", e)
        continue
    
    if 'result' in recebe and len(recebe['result']) > 0:
        for data in recebe['result']:
            Thread(target=process_message, args=(data,)).start()
            Thread(target=del_update, args=(data,)).start()
    sleep(3)
