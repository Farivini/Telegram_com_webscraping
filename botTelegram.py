import json
import requests
from time import sleep
from threading import Thread,Lock       #Lock faz uma thread nao passar uma em cima da outra

from selenium import webdriver
from selenium.webdriver.common.keys import Keys






global config
config = {"url":"https://api.telegram.org/botTOKEN DO SEU BOT/", "lock":Lock(), 'url_file': 'https://api.telegram.org/file/bot1244807427:AAFURjNX9UmYowL-eMR89_-mVHX3SqwD1D0/'}


def del_update(data):
    global config
    print('Deletando mensagem id ' + str(data['update_id'])  )
    ''' trava e inicia com acquire da THREAD indicada la embaixo'''
    config['lock'].acquire()
    requests.post(config['url']+ 'getUpdates',{'offset': data['update_id']+1})
    ''' libera o request '''
    config['lock'].release()

def enviando_msg(data, msg):
    global config
    '''Novamente colocamos acquire e relase junto com lock'''
    config['lock'].acquire()
    requests.post(config['url']+ 'sendMessage', {'chat_id': data['message']['chat']['id'], 'text': str(msg)})
    config['lock'].release()


def pega_documento(file_path):
    global config
    return requests.get(config['url_file']+str(file_path)).content   #retorna conteudo em bytes

def upload(data,file):
    global config

    formatos = {'png':{'metodo':'sendPhoto', 'send':'photo'},'text':{'metodo':'sendDocument', 'send':'document'}}

    return requests.post(config['url']+ formatos['text' if '.txt' in file else 'png']['metodo'],{'chat_id': data['message']['chat']['id']}, files = {formatos['text' if '.txt' in file else 'png']['send']: open(file, 'rb')}).text

while True:
    recebe =''
    while 'result' not in recebe:
        try:
            ''' a gente pega o que recebe dos dados do telegram e transforma em dict'''
            recebe = json.loads(requests.get(config["url"]+ "getUpdates").text)
            break
        except Exception as e:
            recebe = {'result':[]}
            if 'Failed to establish a new connection' in str(e):
                print('Perca de conexão')
            else:
                print("erro desconhecido")




    if len(recebe['result'])>0:
        for data in recebe['result']:
            '''Colocando qual função para rodar  com target depois argumentos com args e depois start'''
            if data['message']['text'] == '/start':
                Thread(target=enviando_msg, args=(data, 'Bem vindo ao assistente da Vsveiculos ')).start()
                Thread(target=enviando_msg, args=(data, 'Digite apenas a placa , no modelo antigo e sem traços ')).start()
                entrou = 1

            Thread(target=del_update, args=(data, ) ).start()

            if 'document' in data['message']:
               print(json.dumps(data['message'], indent=1))





            elif data['message']['text'] !='/start':
                Thread(target=enviando_msg, args=(data, 'Aguarde ')).start()
                PATH = 'aonde se encontra seu webdriver'  # CAMINHO DO EXECUTAVEL DRIVE DO GOOGLE
                drive = webdriver.Chrome(PATH)                    # ASSINALANDO PARA A VARIAVEL
                drive.get("https://login.audatex.com.br/account/login?returnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Daudatexweb%26redirect_uri%3Dhttps%253A%252F%252Faudatexweb.audatex.com.br%252FAudatex_Home.aspx%26response_mode%3Dform_post%26response_type%3Dcode%2520id_token%26scope%3Dopenid%2520profile%2520offline_access%2520roles%2520usuario_info%2520usuario_detalhes%26state%3DOpenIdConnect.AuthenticationProperties%253DvqnSY24pqEKDaL5eILzcM8oxMNzs2O8_tdVeJ2baTtkn8etKS8_2KfejjphbRwE45DCvq8AMNbqgnSQ-HNbzyeKEvVFiefkXModr6mSNJTu-BSqjXoqlAC27juVSzeS6_4rWEBHYtetcL-RpQaRPS6-Mg263frUnthEAZ9saVmiZRoEJKz_NZFFDUCWeWDKnm6ttkFdOGK9sRjRuQzk1Ufq_o96ARqOsnPb2KzmVo1cllvDzHcbQZjKaAX4EYGJGFElfeQkWotQ8yygKvrPigkHgDvFZjJLdAYfV02DW54w%26nonce%3D637333160557911875.N2Q5NzllMjAtNTFjOC00Y2FiLWFlYTgtOTIxOWQ0MzcwOGEyNjQxZWFjMTUtMjg2MS00YjVhLTljZmUtMmJhMmUyN2I2YjBi%26x-client-SKU%3DID_NET%26x-client-ver%3D1.0.40306.1554")
                titulo = drive.title
                #if titulo == 'Audatex':
                # Acessando automaticamente pelo id do html
                usuario = drive.find_element_by_id("UserName")
                usuario.send_keys("usuario")
                senha = drive.find_element_by_id("Password")
                senha.send_keys("senha")
                senha.send_keys(Keys.RETURN)  # Pressiona enter
                sleep(3)
                verifica = drive.title
                print(verifica)
                #if verifica == 'Audatex Web':
                sinistro = drive.find_element_by_id("lnkSinistro")
                sinistro.click()
                sleep(3)
                buscar = drive.find_element_by_id("lnkBuscarOrcamento")
                buscar.click()
                print(drive.title)
                '''Colocar um aguarde'''

                placas = data['message']['text']

                placa = drive.find_element_by_id("ctl00_cphBody_txtPlacaBuscaAvancada")
                placa.send_keys(placas)
                placa.send_keys(Keys.RETURN)
                sleep(3)
                orcamento = drive.find_element_by_class_name("TableIn")



                orcamento.click()
                '''Buscar se o carro tem Rs'''
                comRs = drive.find_element_by_link_text("Laudo Av. de Danos").click()
                botao = drive.find_element_by_id("btnVisualizar").click()
                guiaLaudo = drive.window_handles
                drive.switch_to.window(guiaLaudo[1])
                drive.fullscreen_window()

                fotoLaudo= drive.get_screenshot_as_file("Laudo.png")
                upload(data, "Laudo.png")
                sleep(2)
                drive.switch_to.window(guiaLaudo[0])
                sleep(2)

                imagem = drive.find_element_by_id("btnVisualizarImagem")
                imagem.click()
                guias = drive.window_handles  # lista de guias
               # print(guias)   coloca em uma lista as guias
                rolar = drive.switch_to.window(guias[2])  # pega a segunda guia aberta apos o click
                drive.fullscreen_window()  # coloca a tela em fullscreen

                foto = []
                foto = drive.get_screenshot_as_file("carro.png")
                #print(placa)
                print(upload(data, 'carro.png'))
                rolar = drive.find_element_by_tag_name("html")
                rolar.send_keys(Keys.PAGE_DOWN)
                foto2 = drive.get_screenshot_as_file("carro2.png")
                upload(data, 'carro2.png')
                sleep(1)
                rolar.send_keys(Keys.PAGE_DOWN)
                foto3 = drive.get_screenshot_as_file("carro3.png")
                upload(data, "carro3.png")
                #foto = drive.get_screenshot_as_file("carro.png")
                #drive.quit()


                '''perguntar se quer continuar ou para 
                if drive.title != 'Audatex Web - Orçamentação':
                   print(json.dumps(data, indent =1))
                   Nessa Thread vamos deixar ele controlar a função que envia a mensagem 
                   Podemos colocar um if para filtrar
                   #if data['message']['text'] == 'oi':
                   #imagem = open('NUVEM.jpg')
                   Thread(target=enviando_msg, args=(data, '-------')).start()
                if drive.find_element_by_class_name("TableIn")== False:
                   drive.quit()'''


                enviando_msg(data, "Pronto! Para consultar outra  e só mandar mais uma placa  🏎 .")
            sleep(3)


            entrou = 2