#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import pdfkit
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import tabula
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os




try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version . To view the "
        f" version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.ext import Updater


config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf.exe")






# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
async def Marca(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text("Generando Archivo!")
    document = open('loading.png', 'rb')
    await context.bot.send_photo(chat_id,document)
    print(update.message.text.lower()[7:])
    producto=update.message.text.lower()[7:]
    #Request del archivo Actual de la tienda.
    r = requests.get('https://outlettecnologico.cl/listaPrecios.pdf')
    #Se crea el archivo Metadata.pdf donde se almacena el archivo actual de la tienda.
    with open('metadata.pdf', 'wb') as f:
          f.write(r.content)
    #Archivo PDF metadata.pdf pada a csv, para ser cargado a DataFrame   
    tabula.convert_into('metadata.pdf', "output.csv", output_format="csv", pages='all')
    #Carga a DataFrame   
    df2=pd.read_csv('output.csv',header=[0],encoding ="ISO-8859-1") 
    #Archivo PDF List.pdf pada a csv, para ser cargado a DataFrame   
    tabula.convert_into('List.pdf', "output2.csv", output_format="csv", pages='all')
    #Carga a DataFrame   
    df=pd.read_csv('output2.csv',header=[0],encoding ="ISO-8859-1")
    #Seleccion de SKU de Lista Historica.
    x = df['SKU'].values.tolist()
    lis=[]
    #Se almacenan los SKU que no estan presentes en Archivo Historico.
    for i in range(len(df2)):
        sku=df2.loc[i, "SKU"]
        Marca=str(df2.loc[i, "Marca"])
       
        if sku not in x and producto.lower() in Marca.lower() : 
            print(Marca)
            lis.append(sku) 
    #Se hace filtro por SKU.
    df3=df2.loc[df2['SKU'].isin(lis)]
    #Se genera HTML para ser transformado a PDF
    df3.to_html('test.html')
    #PDF
    pdfkit.from_file('test.html', 'Lista.pdf')
    document = open('Lista.pdf', 'rb')
    await context.bot.send_document(chat_id, document)
    await update.message.reply_text("Archivo Enviado!")

async def Producto2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text("Generando Archivo!")
    document = open('loading.png', 'rb')
    await context.bot.send_photo(chat_id,document)
    print(update.message.text.lower()[10:])
    producto=update.message.text.lower()[10:]
    #Request del archivo Actual de la tienda.
    r = requests.get('https://outlettecnologico.cl/listaPrecios.pdf')
    #Se crea el archivo Metadata.pdf donde se almacena el archivo actual de la tienda.
    with open('metadata.pdf', 'wb') as f:
          f.write(r.content)
    #Archivo PDF metadata.pdf pada a csv, para ser cargado a DataFrame   
    tabula.convert_into('metadata.pdf', "output.csv", output_format="csv", pages='all')
    #Carga a DataFrame   
    df2=pd.read_csv('output.csv',header=[0],encoding ="ISO-8859-1") 
    #Archivo PDF List.pdf pada a csv, para ser cargado a DataFrame   
    tabula.convert_into('List.pdf', "output2.csv", output_format="csv", pages='all')
    #Carga a DataFrame   
    df=pd.read_csv('output2.csv',header=[0],encoding ="ISO-8859-1")
    #Seleccion de SKU de Lista Historica.
    x = df['SKU'].values.tolist()
    lis=[]
    #Se almacenan los SKU que no estan presentes en Archivo Historico.
    for i in range(len(df2)):
        sku=df2.loc[i, "SKU"]
        Nombre=str(df2.loc[i, "Nombre"])
       
        if sku not in x and producto.lower() in Nombre.lower() : 
            print(Nombre)
            lis.append(sku) 
    #Se hace filtro por SKU.
    df3=df2.loc[df2['SKU'].isin(lis)]
    #Se genera HTML para ser transformado a PDF
    df3.to_html('test.html')
    #PDF
    pdfkit.from_file('test.html', 'Lista.pdf')
    document = open('Lista.pdf', 'rb')
    await context.bot.send_document(chat_id, document)
    await update.message.reply_text("Archivo Enviado!")
async def Producto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text("Generando Archivo!")
    document = open('loading.png', 'rb')
    await context.bot.send_photo(chat_id,document)
    print(update.message.text.lower()[10:])
    producto=update.message.text.lower()[10:]
    #Request del archivo Actual de la tienda.
    r = requests.get('https://outlettecnologico.cl/listaPrecios.pdf')
    #Se crea el archivo Metadata.pdf donde se almacena el archivo actual de la tienda.
    with open('metadata.pdf', 'wb') as f:
          f.write(r.content)
    #Archivo PDF metadata.pdf pada a csv, para ser cargado a DataFrame   
    tabula.convert_into('metadata.pdf', "output.csv", output_format="csv", pages='all')
    #Carga a DataFrame   
    df2=pd.read_csv('output.csv',header=[0],encoding ="ISO-8859-1") 
    #Archivo PDF List.pdf pada a csv, para ser cargado a DataFrame   
    tabula.convert_into('List.pdf', "output2.csv", output_format="csv", pages='all')
    #Carga a DataFrame   
    df=pd.read_csv('output2.csv',header=[0],encoding ="ISO-8859-1")
    #Seleccion de SKU de Lista Historica.
    x = df['SKU'].values.tolist()
    lis=[]
    #Se almacenan los SKU que no estan presentes en Archivo Historico.
    for i in range(len(df2)):
        sku=df2.loc[i, "SKU"]
        Nombre=str(df2.loc[i, "Nombre"])
        if producto.lower() in Nombre.lower() : 
            print(Nombre)
            lis.append(sku) 
    #Se hace filtro por SKU.
    df3=df2.loc[df2['SKU'].isin(lis)]
    #Se genera HTML para ser transformado a PDF
    df3.to_html('test.html')
    #PDF
    pdfkit.from_file('test.html', 'Lista.pdf')
    document = open('Lista.pdf', 'rb')
    os.rename("metadata.pdf", "List.pdf")    
    await context.bot.send_document(chat_id, document)
    await update.message.reply_text("Archivo Enviado!")

async def Lista(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text("Generando Archivo!")
    document = open('loading.png', 'rb')
    await context.bot.send_photo(chat_id,document)

  
    #Archivo PDF metadata.pdf pada a csv, para ser cargado a DataFrame   
    tabula.convert_into('metadata.pdf', "output.csv", output_format="csv", pages='all')
    #Carga a DataFrame   
    df2=pd.read_csv('output.csv',header=[0],encoding ="ISO-8859-1") 
    #Archivo PDF List.pdf pada a csv, para ser cargado a DataFrame   
    tabula.convert_into('List.pdf', "output2.csv", output_format="csv", pages='all')
    #Carga a DataFrame   
    df=pd.read_csv('output2.csv',header=[0],encoding ="ISO-8859-1")
    #Seleccion de SKU de Lista Historica.
    x = df['SKU'].values.tolist()
    lis=[] 
    #Se almacenan los SKU que no estan presentes en Archivo Historico.
    for a in df2['SKU']:
      if a not in x: 
        lis.append(df2.loc[df2['SKU'] == a]['SKU'].values[0] )
    #Se hace filtro por SKU.
    df3=df2.loc[df2['SKU'].isin(lis)]
    #Se genera HTML para ser transformado a PDF
    df3.to_html('test.html')
    #PDF
    pdfkit.from_file('test.html', 'Lista.pdf', configuration=config)
    document = open('Lista.pdf', 'rb')




    await context.bot.send_document(chat_id, document)
    await update.message.reply_text("Archivo Enviado!")



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
   # await context.bot.send_message(chat_id='1481376283', text='One message every minute')
    #await context.bot.send_message(chat_id='1481376283', text='Generando') #5812124182
    #document = open('loading.png', 'rb')
    #await context.bot.send_photo('1481376283',document)

    #Request del archivo Actual de la tienda.
    r = requests.get('https://outlettecnologico.cl/listaPrecios.pdf')
    #Se crea el archivo Metadata.pdf donde se almacena el archivo actual de la tienda.
    with open('metadata.pdf', 'wb') as f:
          f.write(r.content)
    #Archivo PDF metadata.pdf pada a csv, para ser cargado a DataFrame   
    tabula.convert_into('metadata.pdf', "output.csv", output_format="csv", pages='all')
    #Carga a DataFrame   
    df2=pd.read_csv('output.csv',header=[0],encoding ="ISO-8859-1") 
    #Archivo PDF List.pdf pada a csv, para ser cargado a DataFrame   
    tabula.convert_into('List.pdf', "output2.csv", output_format="csv", pages='all')
    #Carga a DataFrame   
    df=pd.read_csv('output2.csv',header=[0],encoding ="ISO-8859-1")
    #Seleccion de SKU de Lista Historica.
    x = df['SKU'].values.tolist()
    lis=[]
    #Se almacenan los SKU que no estan presentes en Archivo Historico.
    for a in df2['SKU']: 
      if a not in x:
        lis.append(df2.loc[df2['SKU'] == a]['SKU'].values[0] )
    #Se hace filtro por SKU.
    df3=df2.loc[df2['SKU'].isin(lis)]
    #Se genera HTML para ser transformado a PDF
    df3.to_html('test.html')
    #PDF
    pdfkit.from_file('test.html', 'Lista.pdf')
    document = open('Lista.pdf', 'rb')
    isExist = os.path.exists("metadata.pdf")
    print("len: "+ str(len(lis)))
    if len(lis) == 0:
        os.remove("metadata.pdf")
    else:
        os.remove("List.pdf")
        os.rename("metadata.pdf", "List.pdf")    
        os.remove("output.csv")
        os.remove("output2.csv")
        await context.bot.send_document('1481376283', document)
        await context.bot.send_message(chat_id='1481376283', text='Enviado')
        await context.bot.send_document('5812124182', document)
        await context.bot.send_message(chat_id='5812124182', text='Enviado')

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5462188589:AAH9xKvjAr4UPkb1wJneXO2gjeWfmrNdIZQ").build()
    job_queue = application.job_queue
    job_minute = job_queue.run_repeating(callback_minute, interval=60, first=10)


    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lista", Lista))
    application.add_handler(CommandHandler("producto", Producto))
    application.add_handler(CommandHandler("marca", Marca))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()