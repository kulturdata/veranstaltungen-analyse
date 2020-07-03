"""
Dieses Script nutzt Selenium, um auf muenchen.de alle Veranstaltungen anzeigen zu lassen.
Es werden jedoch nur die erstmaligen VAs auf der Webseite angezeigt. Wenn VAs an mehreren Tagen stattfinden,
werden sie nur beim ersten Mal gescrappt.
"""

from selenium import webdriver
from time import sleep
from random import randint

# Files
web_m_file = 'web_m_file.html'


# Bei erstmaliger Nutzung:
# driver muss in user/local/bin gespeichert werden
# und in Einstellungen unter Sicherheit muss das Öffnen bestätigt werden

wait = randint(3,9) # Hat sich als passende Ladezeit ergeben

# Version ohne das Öffnen der Software Chrome (so auch für Cloud-Anwendung geeignet)
# Wenn man die Steuerung sehen will, muss man nur die optionen herausnehmen und unten aus der Klammer löschen
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

driver.get("https://www.muenchen.de/veranstaltungen/event/listing.html?what=&where=&from=&to=")
sleep(wait)

# 1. So oft auf Mehr anzeigen drücken, bis Button nicht mehr da ist
try:
    button = driver.find_element_by_id('event-list-showmore')
except:
    print ('Button konnte nicht gefunden werden')

# zählt Fehlversuche
z = []
i = []
def mehr_anzeigen():
    try:
        button.click()
        z.append('geklickt')
        wait = randint(3,9)
        sleep(wait)
        mehr_anzeigen()
    except:
        i.append('fehler')
        print ('Button klicken nicht möglich. Fehlversucht: ', len(i))
        sleep(randint(3,9))

        if len(i) < 6:
            print ('Startet erneut')
            mehr_anzeigen()
        else:
            print ('🎉 Alle Veranstaltungen wurden geladen', len(z), '-mal wurde der Button geklickt')
            print ('Jetzt wird die html Datei erstellt')

mehr_anzeigen()


# 2. Diese gesamte Page als html abspeichern
soup_web = driver.page_source
with open(web_m_file, 'w+') as web_m:
    web_m.write(str(soup_web))
    print ('Datei ' + str(web_m_file) + ' wurde erstellt' )