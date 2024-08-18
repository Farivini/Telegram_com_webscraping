# Telegram_com_webscraping





# 🤖 Bot do Telegram com Web Scraping 🕸️

Este repositório contém um script em Python desenvolvido por **Vinicius Farineli Freire** que implementa um bot no Telegram capaz de realizar tarefas de web scraping. O projeto é um exemplo prático de como integrar um bot do Telegram com técnicas de coleta automatizada de dados de websites.

## 🎯 Objetivo do Projeto

O objetivo principal deste projeto é demonstrar como criar um bot no Telegram que responde a comandos do usuário realizando web scraping para extrair e retornar informações relevantes de páginas web. Este tipo de aplicação pode ser usado para uma variedade de propósitos, como monitoramento de preços, extração de notícias ou coleta de dados específicos de sites.

## 🗂️ Arquivo Principal

- `botTelegram.py`: Script Python que contém a implementação do bot do Telegram com a funcionalidade de web scraping.

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem de programação usada para o desenvolvimento do bot.
- **Telegram Bot API**: Utilizada para criar e gerenciar o bot no Telegram.
- **BeautifulSoup**: Biblioteca Python para extração de dados de documentos HTML e XML.
- **Requests**: Biblioteca para realizar requisições HTTP em Python, usada para acessar páginas web.

## 🚀 Como Funciona

1. **Criação do Bot**: O script começa configurando um bot no Telegram usando a API do Telegram. É necessário obter um token de acesso fornecido pelo BotFather no Telegram.
2. **Web Scraping**: Quando o bot recebe um comando do usuário, ele realiza uma requisição HTTP para a URL especificada, faz a análise da página usando BeautifulSoup e extrai as informações desejadas.
3. **Resposta ao Usuário**: As informações extraídas são formatadas e enviadas de volta ao usuário via Telegram.

### 📽️ Demonstração

Confira abaixo um GIF mostrando o bot em ação:

![Bot Rodando](20201218_223055.gif) 


## 🛠️ Como Executar o Projeto

1. Clone o repositório para sua máquina local:

   ```bash
   git clone https://github.com/Farivini/Telegram_com_webscraping.git
   ```

2. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

3. Adicione o token do seu bot no script `botTelegram.py`.

4. Execute o script:

   ```bash
   python botTelegram.py
   ```

5. Abra o Telegram e inicie uma conversa com o seu bot para testar a funcionalidade de web scraping.

## 🌟 Possíveis Melhorias

- **Aprimorar o Web Scraping**: Adicionar funções para lidar com diferentes tipos de sites e conteúdo dinâmico (JavaScript).
- **Novos Comandos**: Implementar mais comandos para extrair diferentes tipos de dados ou monitorar mudanças em sites específicos.
- **Segurança e Tratamento de Erros**: Melhorar a robustez do bot, incluindo mais verificações de erros e segurança ao lidar com URLs e entradas de usuários.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

