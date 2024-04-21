
# from flask import Flask, render_template, request
# import requests
# from bs4 import BeautifulSoup
# import smtplib

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         url = request.form.get('url')
#         verifica_preco(url)
#         return render_template('index.html', message='E-mail enviado!')
#     return render_template('index.html', message='')

# def verifica_preco(URL):
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, 'html.parser')
    
#     title_element = soup.find('h1', class_='ui-pdp-title')
#     if title_element is None:
#       print("Não foi possível encontrar o título do produto.")
#       return
#     title = title_element.get_text()


#     price = soup.find('span', class_ = 'andes-money-amount__fraction').get_text()
    
#     converted_price = float(price[0:5])

#     if(converted_price < 500.00):
#         envia_email(URL)

# def envia_email(URL):
#     print(URL)
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()

#     server.login('rjr89000@gmail.com', 'hnrz vlov rpec jgnv')

#     assunto = 'Preco caiu!'
#     corpo = f'Verifique o link do mercado livre {URL}'

#     msg = f"Subject: {assunto}\n\n{corpo}"

#     server.sendmail(
#         'rjr89000@gmail.com',
#         # 'rjr89000@outlook.com',
#         'gleicefrancielecosta@gmail.com',
#         msg,
        
#     )
#     print('E-mail enviado!')

#     server.quit()

# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, render_template, request
# import requests
# from bs4 import BeautifulSoup
# import smtplib
# import schedule
# import time
# import threading

# app = Flask(__name__)

# url_to_check = None

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     global url_to_check
#     if request.method == 'POST':
#         url_to_check = request.form.get('url')
#         return render_template('index.html', message='Monitoramento iniciado!')
#     return render_template('index.html', message='')

# def verifica_preco():
#     global url_to_check
#     if url_to_check is None:
#         return

#     URL = url_to_check
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, 'html.parser')
    
#     title_element = soup.find('h1', class_='ui-pdp-title')
#     if title_element is None:
#       print("Não foi possível encontrar o título do produto.")
#       return
#     title = title_element.get_text()

#     price = soup.find('span', class_ = 'andes-money-amount__fraction').get_text()
    
#     converted_price = float(price[0:5])

#     if(converted_price < 500.00):
#         print('verificou e vai mandar o email!!! \n\n')
#         envia_email(URL)

# def envia_email(URL):
#     print(URL)
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()

#     server.login('rjr89000@gmail.com', 'hnrz vlov rpec jgnv')

#     assunto = 'Preco caiu!'
#     corpo = f'Verifique o link do mercado livre {URL}'

#     msg = f"Subject: {assunto}\n\n{corpo}"

#     server.sendmail(
#         'rjr89000@gmail.com',
#         'gleicefrancielecosta@gmail.com',
#         msg,
        
#     )
#     print('E-mail enviado!')

#     server.quit()

# def run_schedule():
#     while 1:
#         schedule.run_pending()
#         time.sleep(1)

# if __name__ == '__main__':
#     schedule.every(10).seconds.do(verifica_preco)
#     t = threading.Thread(target=run_schedule)
#     t.start()
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import smtplib
import schedule
import time
import threading

app = Flask(__name__)

url_to_check = None
emails_sent = 0
# monitoring = False

@app.route('/', methods=['GET', 'POST'])
def index():
    global url_to_check
    if request.method == 'POST':
        url_to_check = request.form.get('url')
        # monitoring = True
        return render_template('index.html', message='Monitoramento iniciado!', emails_sent=emails_sent)
    return render_template('index.html', message='', emails_sent=emails_sent)


@app.route('/stop', methods=['POST'])
def stop():
    global url_to_check
    # monitoring = False
    url_to_check = None
    return redirect(url_for('index'))


def verifica_preco():
    global url_to_check
    if url_to_check is None:
        return

    URL = url_to_check
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    title_element = soup.find('h1', class_='ui-pdp-title')
    if title_element is None:
      print("Não foi possível encontrar o título do produto.")
      return
    title = title_element.get_text()

    price = soup.find('span', class_ = 'andes-money-amount__fraction').get_text()
    
    converted_price = float(price[0:5])

    if(converted_price < 500.00):
        print('verificou e vai mandar o email!!! \n\n')
        envia_email(URL)

def envia_email(URL):
    global emails_sent
    print(URL)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('rjr89000@gmail.com', 'hnrz vlov rpec jgnv')

    assunto = 'Preco caiu!'
    corpo = f'Verifique o link do mercado livre {URL}'

    msg = f"Subject: {assunto}\n\n{corpo}"

    server.sendmail(
        'rjr89000@gmail.com',
        'rjr89000@outlook.com',
        msg,
        
    )
    print('E-mail enviado!')
    emails_sent += 1

    server.quit()

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    schedule.every(10).seconds.do(verifica_preco)
    t = threading.Thread(target=run_schedule)
    t.start()
    app.run(debug=True)

