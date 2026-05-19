import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Webhook Discord
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1502659870749360319/39p3pbrD2FuM1ACyo6QzlpU-ZHZTm4EpdbtHZa94GsklZb2_M0mG2qfATXiNEOjT9skU"

def send_discord_notification(message):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"Errore Discord: {e}")

# Configura il WebDriver per Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Vai al sito
driver.get("https://compraticketspro.alhambra-patronato.es/reservarEntradas.aspx?opc=177&gid=432&lg=it-IT&ca=142-426&m=webpro")

print("Attendi che il login venga eseguito manualmente e premi il pulsante una volta.")

notifica_inviata = False  # Evita notifiche duplicate

# Loop per cercare il pulsante e premere in loop
while True:
    try:
        button = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentMaster1_ucReservarEntradasBaseAlhambra1_btnIrPaso2"]')
        if button.is_enabled():
            button.click()
            print("Pulsante cliccato automaticamente!")
        else:
            print("Il pulsante è disabilitato, attendo...")
    except:
        print("Pulsante non trovato, il bot continua a cercare...")

    # Controlla se appare il bottone "Accettare" (pagina di pagamento)
    try:
        paga = driver.find_element(By.XPATH, '//*[@id="divImgAceptar"]')
        if paga.is_displayed() and not notifica_inviata:

            # Estrai importo dal div .ticket-header
            importo = "N/D"
            try:
                importo_elem = driver.find_element(By.CSS_SELECTOR, ".ticket-header .price .right p")
                importo = importo_elem.text.strip().replace("\xa0", " ")
            except:
                pass

            print(f"💳 Bottone Accettare rilevato! Importo: {importo}")
            send_discord_notification(
                f"💳 **PAGAMENTO PRONTO!**\n"
                f"💶 Importo: **{importo}**\n"
                f"Il bottone 'Accettare' è apparso — vai a completare l'acquisto subito!"
            )
            notifica_inviata = True
    except:
        notifica_inviata = False  # Reset quando il bottone sparisce

    time.sleep(0.5)