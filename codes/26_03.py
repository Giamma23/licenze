from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configura il WebDriver per Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Vai al sito
driver.get("https://compraticketspro.alhambra-patronato.es/reservarEntradas.aspx?opc=177&gid=432&lg=it-IT&ca=142-426&m=webpro")

print("Attendi che il login venga eseguito manualmente e premi il pulsante una volta.")

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
    
    time.sleep(0.5)  # Evita di sovraccaricare il sito con troppi click
