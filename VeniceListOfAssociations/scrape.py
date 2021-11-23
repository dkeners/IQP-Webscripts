import requests
import pandas as pd

# Constant variable functions
# URL for all: https://portale.comune.venezia.it/sites/all/modules/yui_venis/associazioni.php
# PARAMS for all: ?tipo=JSON
# At time of coding (22 Nov 2021) there were 3534 total associazioni listed
url = 'https://portale.comune.venezia.it/sites/all/modules/yui_venis/associazioni.php'
# URL for individual: https://portale.comune.venezia.it/sites/all/modules/yui_venis/associazioniDetail.php
# PARAMS for individual: ?tipo=JSON&numero=3
indiv_url = 'https://portale.comune.venezia.it/sites/all/modules/yui_venis/associazioniDetail.php'
params = {'tipo': 'JSON'}
rows = []

# Create a second row with english translations
rows.append({"Numero di iscrizione all'albo": "Registered number",
             'Denominazione': 'Name',
             'Data iscrizione': 'Registration / resolution date',
             'Numero delibera': 'Resolution number',
             'Data cessazione': 'End date',
             'Municipalità': 'Municipalities',
             'Attività': 'Activities',
             'Scopo / intenti': 'Purpose / intent',
             'Indirizzo': 'Street address',
             'Email': 'E-mail',
             'Sito web': 'Website',
             'Presidente': 'President',
             'Data domanda': 'Application date',
             'Protocollo domanda': 'Application protocol',
             'Telefono': 'Phone number',
             'Fiscale codice': 'Tax code',
             'Iva partita': 'VAT number'})

# create column headers
cols = ["Numero di iscrizione all'albo", 'Denominazione',
        'Data iscrizione', 'Numero delibera', 'Data cessazione',
        'Municipalità', 'Attività', 'Scopo / intenti', 'Indirizzo',
        'Email', 'Sito web', 'Presidente', 'Data domanda',
        'Protocollo domanda', 'Telefono',
        'Fiscale codice', 'Iva partita']

# Something here
r = requests.get(url, params=params)
r.encoding = 'utf-8'

# Parse JSON file of individual events
results = r.json()


def scrapeCurrentData(itemNum=0, end=0):

    try:
        # Define the parameters
        params['numero'] = itemNum

        r = requests.get(indiv_url, params=params)
        r.encoding = 'utf-8'

    except Exception as e:
        # Make dataframe
        df = pd.DataFrame(rows, columns=cols)

        # write dataframe to csv
        df.to_csv('associazioni_utf-8' + str(itemNum) + '.csv', encoding='utf-8-sig')
        print('associazioni_utf-8' + str(itemNum) + '.csv has been made in the folder and can now be accessed.')

        raise e

    # Parse JSON file of individual events
    indiv_results = r.json()

    # create defaults for each that could be empty
    deliberaNumero = indiv_results['deliberaNumero'] if 'deliberaNumero' in indiv_results else ''
    cessazioneData = results['associazioni'][itemNum]['cessazioneData'] if 'cessazioneData' in results['associazioni'][itemNum] else ''
    municipalita = results['associazioni'][itemNum]['municipalita'] if 'municipalita' in results['associazioni'][itemNum] else ''
    attivita = results['associazioni'][itemNum]['attivita'] if 'attivita' in results['associazioni'][itemNum] else ''
    specifica = indiv_results['specifica'] if 'specifica' in indiv_results else ''
    indirizzo = indiv_results['indirizzo'] if 'indirizzo' in indiv_results else ''
    email = indiv_results['email'] if 'email' in indiv_results else ''
    sitoWeb = indiv_results['sitoWeb'] if 'sitoWeb' in indiv_results else ''
    presidente = indiv_results['presidente'] if 'presidente' in indiv_results else ''
    domandaData = indiv_results['domandaData'] if 'domandaData' in indiv_results else ''
    domandaProtocollo = indiv_results['domandaProtocollo'] if 'domandaProtocollo' in indiv_results else ''
    telefono = indiv_results['telefono'] if 'telefono' in indiv_results else ''
    codiceFiscale = indiv_results['codiceFiscale'] if 'codiceFiscale' in indiv_results else ''
    partitaIva = indiv_results['partitaIva'] if 'partitaIva' in indiv_results else ''

    rows.append({"Numero di iscrizione all'albo": results['associazioni'][itemNum]['iscrizioneNumero'],
                 'Denominazione': results['associazioni'][itemNum]['denominazione'],
                 'Data iscrizione': results['associazioni'][itemNum]['deliberaData'],
                 'Numero delibera': deliberaNumero,
                 'Data cessazione': cessazioneData,
                 'Municipalità': municipalita,
                 'Attività': attivita,
                 'Scopo / intenti': specifica,
                 'Indirizzo': indirizzo,
                 'Email': email,
                 'Sito web': sitoWeb,
                 'Presidente': presidente,
                 'Data domanda': domandaData,
                 'Protocollo domanda': domandaProtocollo,
                 'Telefono': telefono,
                 'Fiscale codice': codiceFiscale,
                 'Iva partita': partitaIva})

    if itemNum == end:

        # Make dataframe
        df = pd.DataFrame(rows, columns=cols)

        # write dataframe to csv
        df.to_csv('associazioni_utf-8.csv', encoding='utf-8-sig')
        print('associazioni_utf-8.csv has been made in the folder and can now be accessed.')

    else:
        itemNum += 1
        if itemNum % 20 == 0:
            print(str(itemNum) + " points logged")
        scrapeCurrentData(itemNum, end)


# 3534 at current time
scrapeCurrentData(itemNum=3367, end=3533)
