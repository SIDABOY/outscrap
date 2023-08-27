import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import tabula
import numpy as np
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

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


    
async def caca(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    r = requests.get('https://outlettecnologico.cl/listaPrecios.pdf')
    with open('metadata.pdf', 'wb') as f:
        f.write(r.content)
    user2="a"
    df2 = tabula.read_pdf('metadata.pdf',pages ='all')
    tabula.convert_into('metadata.pdf', "output.csv", output_format="csv", pages='all')
    df2=pd.read_csv('output.csv',header=[0],encoding="latin-1",sep=',') 
    print("HEllo")
    df=pd.read_csv('output2.csv',header=[0],encoding="latin-1",sep=',') 

    x = df['SKU'].values.tolist()
    lis=[]
    for a in df2['SKU']:
        if a not in x:
            lis.append(df2.loc[df2['SKU'] == a]['SKU'].values[0] )
            
    df3=df2.loc[df2['SKU'].isin(lis)]
    df3.to_excel('hola.xlsx')
    chat_id = update.message.chat_id
    document = open('output2.csv', 'rb')
    await context.bot.send_document(chat_id, document)
    await update.message.reply_html(
        
        rf"Documento Enviado  {user.mention_html()}!"+user2,
        reply_markup=ForceReply(selective=True)

    )

async def falabella(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    page = requests.get("https://www.falabella.com/falabella-cl/category/cat70057/Notebooks?facetSelected=true&f.product.attribute.Tipo=Gamers")
    soup = BeautifulSoup(page.text, "lxml")
    for a in soup.findAll('div', attrs={'class':'jsx-4001457643 search-results-list'}):

         await update.message.reply_text(a.find('b', attrs={'class':'jsx-4221770651'}).get_text())
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5525661793:AAGpyMWDd_MixvkrvqvA45UQeTeKzMd0iR4").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("caca", caca))
    application.add_handler(CommandHandler("falabella", falabella))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
