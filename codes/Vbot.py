import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Dati per il login
EMAIL = "gianmarcodin23@gmail.com"
PASSWORD = "Gianmarcodin23."

# Webhook Discord
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1356320008501858497/tb-quaAhM--Rsk-thdjRmD0hY6ya9T-YhWN7qxc732dlSWtJkyGHRi3hmLKf2bUTnZlp"

# URL della pagina dei biglietti
URL = "https://compraticketspro.alhambra-patronato.es/reservarEntradas.aspx?opc=177&gid=432&lg=it-IT&ca=142-426&m=webpro"

# Configurazione Selenium
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def send_discord_notification(message):
    """Invia una notifica su Discord"""
    try:
        payload = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("📩 Messaggio inviato su Discord!")
        else:
            print(f"❌ Errore nell'invio su Discord: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Errore nella connessione a Discord: {e}")

def accept_cookies():
    """Accetta i cookie se presenti"""
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='ctl00_lnkAceptarTodoCookies_Info']"))
        ).click()
        print("✅ Cookie accettati.")
    except:
        print("⚠️ Nessun cookie da accettare.")

def login():
    """Esegue il login se necessario"""
    print("🔑 Controllo il login...")
    driver.get(URL)
    time.sleep(3)
    accept_cookies()

    try:
        email_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='ctl00_txtLoginEmail']")))
        print("🔐 Login richiesto. Inserisco le credenziali...")
        email_input.send_keys(EMAIL)
        driver.find_element(By.XPATH, "//*[@id='ctl00_txtLoginPassword']").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//*[@id='ctl00_btnLogin']").click()
        print("✅ Login effettuato!")
        time.sleep(5)
    except:
        print("✅ Sei già loggato.")

def click_passo_1():
    """Premi 'Vai al Passaggio 1' se appare"""
    try:
        bottone_passo1 = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='ctl00_ContentMaster1_ucReservarEntradasBaseAlhambra1_btnIrPaso1']"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", bottone_passo1)
        driver.execute_script("arguments[0].click();", bottone_passo1)
        print("✅ Cliccato su 'Vai al Passaggio 1'!")
        time.sleep(3)
    except:
        print("✅ Nessun bisogno di premere 'Vai al Passaggio 1'.")

def check_tickets():
    """Controlla la disponibilità dei biglietti senza ricaricare la pagina"""
    print("🔄 Controllo la disponibilità dei biglietti...")
    try:
        click_passo_1()

        mese_testo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "calendario_titulo"))
        ).text
        print(f"📅 Mese attuale: {mese_testo}")

        giorni_disponibili = []
        for giorno in driver.find_elements(By.CLASS_NAME, "calendario_padding"):
            if "dispo" in giorno.get_attribute("class") or "ult-plaza" in giorno.get_attribute("class"):
                link = giorno.find_element(By.TAG_NAME, "a")
                numero_giorno = link.text.strip()
                giorni_disponibili.append(f"{numero_giorno} {mese_testo}")

        if giorni_disponibili:
            print("✅ Ho trovato biglietti disponibili!")
            print(f"🎟️ Giorni disponibili: {giorni_disponibili}")

            messaggio = f"🎟️ **Biglietti disponibili!** 🎟️\n📅 Giorni: {', '.join(giorni_disponibili)}\n🔗 [Compra qui]({URL})"
            print("📩 Invio notifica su Discord...")
            send_discord_notification(messaggio)
        else:
            print("❌ Nessun biglietto disponibile.")

    except Exception as e:
        print(f"⚠️ Errore nel controllo dei biglietti: {e}")

def next_month():
    """Clicca sulla freccia avanti"""
    try:
        print("➡️ Clicco sulla freccia avanti...")
        avanti_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='ctl00_ContentMaster1_ucReservarEntradasBaseAlhambra1_ucCalendarioPaso1_calendarioFecha']/tbody/tr[1]/td/table/tbody/tr/td[3]/a/img"))
        )
        driver.execute_script("arguments[0].click();", avanti_button)
        time.sleep(3)
        click_passo_1()
    except Exception as e:
        print(f"❌ Errore nel clic sulla freccia avanti: {e}")

def previous_month():
    """Clicca sulla freccia indietro"""
    try:
        print("⬅️ Clicco sulla freccia indietro...")
        indietro_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='ctl00_ContentMaster1_ucReservarEntradasBaseAlhambra1_ucCalendarioPaso1_calendarioFecha']/tbody/tr[1]/td/table/tbody/tr/td[1]/a/img"))
        )
        driver.execute_script("arguments[0].click();", indietro_button)
        time.sleep(3)
        click_passo_1()
    except Exception as e:
        print(f"❌ Errore nel clic sulla freccia indietro: {e}")

def loop_marzo_aprile():
    """Ciclo tra marzo e aprile per 4 volte, poi aggiorna la pagina e ripete"""
    while True:
        login()
        for _ in range(4):
            check_tickets()
            next_month()
            check_tickets()
            previous_month()

        print("🔄 Ricarico la pagina e riparto da capo...")
        driver.refresh()
        time.sleep(5)

if __name__ == "__main__":
    loop_marzo_aprile()
