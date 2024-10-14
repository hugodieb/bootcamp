import pandas as pd #pacote leitura de dados
import datetime as dt #pacote de datas
import yfinance as yf #baixar as cotações de graça
from matplotlib import pyplot as plt #pacote de graficos
import mplcyberpunk #estilizar graficos
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart #enviar pacote de emails
from email.mime.base import MIMEBase
from email import encoders

ativos = ["^BVSP", "BRL=X", "PBR-A", "MXRF11.SA"]

hoje = dt.datetime.now()
um_mes_atras = hoje - dt.timedelta(days=30)

dados_mercado = yf.download(ativos, um_mes_atras, hoje)

print(dados_mercado)

# Começar a manipular os dados coletados

print(dados_mercado['Adj Close']) #filtrei pela coluna para os 3 ativos

print(dados_mercado['Adj Close']['PBR-A']) #filtrei pela coluna para o ativo petrobras

dados_fechamento = dados_mercado['Adj Close']

print(dados_fechamento)

dados_fechamento.columns = ['dolar', 'mxfr11', 'petrobras', 'ibovespa']


print("Dados de fechamentos")
print(dados_fechamento) #mudei o nome das colunas

dados_fechamento = dados_fechamento.dropna() #ignora dados vazios

print(dados_fechamento.head(50))

dados_fechamento_mensal = dados_fechamento.resample('M').last() #pegando dados por fechmaneto mensal

print(dados_fechamento_mensal)

dados_fechamento_anual = dados_fechamento.resample('Y').last() #pegando dados fechamento anual

print(dados_fechamento_anual)

retorno_no_ano = dados_fechamento_anual.pct_change().dropna()
retorno_no_mes = dados_fechamento_mensal.pct_change().dropna()
retorno_no_dia = dados_fechamento.pct_change().dropna()

print("## Retorno do ano")
print(retorno_no_ano)
print("## Retorno por mes")
print(retorno_no_mes)
print("## Retorno do dia")
print(retorno_no_dia)


#### Localizar o fechamento do dia anterior, retorno do mes e retorno no ano

# Loc - referenciar elementos a partir do nome
# Iloc - selecionar elementos como uma matriz

retorno_do_dia_dolar_loc = retorno_no_dia.loc['2024-10-11', 'dolar']
retorno_do_dia_dolar_loc = round(retorno_do_dia_dolar_loc * 100, 2)


print('****retorno_do_dia_dolar_loc****')
print(retorno_do_dia_dolar_loc)

###retorno_do_dia_loc = retorno_no_dia.loc['2024-10-08']

print('*******************')
#print(retorno_do_dia_loc)

retorno_do_dia_petrobras_iloc = retorno_no_dia.iloc[5,2]
retorno_do_dia_dolar_iloc = retorno_no_dia.iloc[5,0]

retorno_do_dia_petrobras_iloc = round(retorno_do_dia_petrobras_iloc * 100, 2)
retorno_do_dia_dolar_iloc = round(retorno_do_dia_dolar_iloc * 100, 2)

print('****retorno_do_dia_petrobras_iloc****')
print(retorno_do_dia_petrobras_iloc)

print('****retorno_do_dia_dolar_iloc****')
print(retorno_do_dia_dolar_iloc)


retorno_do_ultimo_dia_ibove = retorno_no_dia.iloc[-1,1]
retorno_do_ultimo_dia_ibove = round(retorno_do_ultimo_dia_ibove * 100, 2)

print('****retorno_do_ultimo_dia_ibovespa_iloc****')
print(retorno_do_ultimo_dia_ibove)

## Vamos fazer os graficos agora

plt.style.use("cyberpunk")

dados_fechamento.plot(y = 'dolar', use_index=True, legend=False)

plt.title("Dolar")

plt.savefig("/home/mint/Projetos/bootcamp/imagens/dolar.png", dpi=300)

plt.show()

#Verifica se existe arquivo .env
load_dotenv()

EMAIL_SERVER_PASSWORD = os.environ.get("EMAIL_SERVER_PASSWORD")
EMAIL_SERVER_HOST = os.environ.get("EMAIL_SERVER_HOST")
EMAIL_SERVER_PORT = os.environ.get("EMAIL_SERVER_PORT")
EMAIL_SERVER_USER = os.environ.get("EMAIL_SERVER_USER")

# Informações do e-mail
email_remetente = "no-reply@micro-app.com.br"
lista_destinatarios = ["hugodieb.py@gmail.com", "hugodieb.hd@gmail.com", "hugodieb.dazloja@gmail.com"]
assunto = "E-mail de Teste via Mailtrap"
corpo_email = f"""
<!DOCTYPE html>
<html>
<head>
  <style>
    .destaque {{
      font-weight: bold;
      color: #FF5733; /* Cor laranja */
    }}
    .detalhes {{
      background-color: #f2f2f2;
      padding: 10px;
      border-radius: 5px;
    }}
  </style>
</head>
<body>
  <p>Prezado <strong>Sr. Diretor</strong>.</p>

  <p>Segue os dados do ultimo relatório do dia <strong>11/10/2024</strong>.</p>

  <div class="detalhes">
    <p> <strong>Petrobras:</strong> </p>
    <p> <span class="destaque">{retorno_do_dia_petrobras_iloc}%</span></p>    
  </div>

  <p>Att.</p>

  <p>Hugo Dieb</p>
</body>
</html>

"""    

# Criar o e-mail
msg = MIMEMultipart()
msg['From'] = email_remetente
msg['To'] = ", ".join(lista_destinatarios)
msg['Subject'] = assunto

# Anexar o arquivo PNG como anexo
caminho_arquivo = '/home/mint/Projetos/bootcamp/imagens/dolar.png'
try:
    with open(caminho_arquivo, "rb") as anexo:
        parte = MIMEBase('application', 'octet-stream')
        parte.set_payload(anexo.read())
        encoders.encode_base64(parte)
        parte.add_header(
            "Content-Disposition",
            f"attachment; filename= {caminho_arquivo.split('/')[-1]}"
        )
        msg.attach(parte)
except Exception as e:
    print(f"Erro ao anexar arquivo: {e}")
    

# Anexar o corpo do e-mail
msg.attach(MIMEText(corpo_email, 'html'))

# Conectar ao servidor SMTP do Mailtrap e enviar o e-mail
try:
    servidor = smtplib.SMTP(EMAIL_SERVER_HOST, EMAIL_SERVER_PORT)
    servidor.starttls()  # Segurança
    servidor.login(EMAIL_SERVER_USER, EMAIL_SERVER_PASSWORD)
    texto = msg.as_string()
    servidor.sendmail(email_remetente, lista_destinatarios, texto)
    print("E-mail enviado com sucesso para Mailtrap!")
except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")
finally:
    servidor.quit()