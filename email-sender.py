import smtplib
import email.message
from dotenv import load_dotenv
import os
from main import dfWeather, dfForecast, city, state
load_dotenv()
# .env apenas para não exibir credenciais
mail = os.getenv("mail")
to = os.getenv("to")
senha = os.getenv("senha")

def enviar_email():  
    #transformando dfs em html para manter o formato de tabela
    dfWeather_html = dfWeather.to_html(index=False)
    dfForecast_html = dfForecast.to_html(index=False)

    corpo_email = f"""
    <p>Temperatural de hoje em {city}</p>
    <p>{dfWeather_html}</p>
    <p>Próximos dias</p>
    <p>{dfForecast_html}</p>
    """

    msg = email.message.Message()
    msg['Subject'] = f"Previsão do tempo em {city},{state}"
    msg['From'] = mail
    msg['To'] = to
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], senha)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

enviar_email()