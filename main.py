"""
--- Dieses Script ist Teil 2 Aber es lädt Teil 1 automatisch. Agiert daher als Hauptskript ---
Es wird die muenchen.de Webseite geladen und dort nach Veranstaltungs-: Titel, Datum, Ort gesucht
Diese Daten werden in ein csv file gespeichert, auf welches die Webseite aufbaut.
"""

from bs4 import BeautifulSoup
import pandas
import datetime


# files
web_m_file = '/home/KulturData/mysite/web_m_file.html'
csv_name = '/home/KulturData/mysite/va_m.csv'


print ('Datei wird erstellt')
import selenium_muenchen # Startet Teil 1 selenium_muenchen.py
print ('Datei wurde erstellt')




# Durchsuchen der lokalen web_m_file mit BeautifulSoup statt immer der orignalen Webseite
# Naming soup beibehalten, um den Code wiederzuverwenden
soup = BeautifulSoup(open(web_m_file), "html.parser")
va_date_raw = soup.find_all('span', attrs={'class': 'eventinfo eventinfo--time'})
va_title_raw = soup.find_all('h2', itemprop='name')
va_ort_raw = soup.find_all('a', attrs={'class': "eventinfo eventinfo--location"})


t_list = []
def va_title():
    # Zieht den VA Titel aus der Webseite und fügt ihn in die Liste t_list ein
    for t in va_title_raw:
        t = t.text
        t_list.append(t)
va_title()


d_list = []
def va_date():
    # Zieht das VA Datum us der Webseite und fügt ihn in die Liste d_list ein
    for d in va_date_raw:
        d = d.text.strip() # Loescht die Spaces
        d = d[4:21] # schränkt auf die nötigen Daten ein: dd.mm.yyyy, hh:mm
        d_list.append(d)
va_date()


o_list = []
def va_ort():
    # Zieht den VA Ort aus der Webseite und fügt ihn in die Liste o_list ein
    for o in va_ort_raw:
        o = o.text
        o_list.append(o)
va_ort()


# Datum des webscrappings hinzufuegen
date_scrapping = datetime.datetime.now().timestamp()

# Dict erstellen
uebersicht = {
    'time': date_scrapping,
    'va_title': t_list,
    'va_datum': d_list,
    'va_ort'  : o_list
    }


# Dict --> DataFrame
df = pandas.DataFrame(uebersicht)
print ('Anzahl an VAs am heutigen', datetime.datetime.now(), '=', len(df.index))

def df_to_csv():
    df.to_csv(csv_name, sep='\t', mode='w+', encoding='utf-8')
    print ('Daten sind in', csv_name, 'geladen')

# Check, ob neue Daten korrekt gezogen wurden
if len(df.index) > 10:
    df_to_csv()
    print ('100 Prozent geschafft!')
else:
    print('Es sind weniger als 10 Veranstaltungen, daher wurde die csv nicht geupdatet. Hier der df:')
    print(df.describe)




