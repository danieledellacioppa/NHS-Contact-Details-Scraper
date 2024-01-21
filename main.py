import requests
from bs4 import BeautifulSoup
import csv

# URL della directory del provider NHS
url = "https://www.england.nhs.uk/publication/nhs-provider-directory/"

# Esegui la richiesta HTTP per ottenere il contenuto della pagina
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Trova tutti i link ai Foundation Trusts
# Assicurati di filtrare solo i link esterni validi
trust_links = [link for link in soup.find_all('a', href=True) if 'http' in link['href']]

# Prepara il file CSV per salvare i dettagli di contatto
with open('nhs_contact_details.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Trust Name', 'Address', 'Telephone', 'Website'])  # Intestazioni delle colonne

    # Per ogni link, visita la pagina e ottieni i dettagli di contatto
    for link in trust_links:
        trust_url = link['href']
        trust_response = requests.get(trust_url)
        trust_soup = BeautifulSoup(trust_response.text, 'html.parser')

        # Cerca il termine "Address" per iniziare a salvare i dettagli
        contact_section = trust_soup.find('h2', string='Contact details')

        if contact_section:
            contact_info = contact_section.find_next('div', class_='rich-text')

            if contact_info:
                # Rimuovi il testo non necessario e estrai solo il nome del Trust
                trust_name = trust_soup.find('h1').get_text().replace('Cookies on the NHS England website', '').strip()

                # Estrai l'indirizzo, il telefono e il sito web come prima
                address = 'Not found'
                telephone = 'Not found'
                website = 'Not found'

                address_heading = contact_info.find('h3', string='Address')
                if address_heading and address_heading.find_next('p'):
                    address = address_heading.find_next('p').get_text(separator='\n').strip()

                telephone_heading = contact_info.find('h3', string='Telephone')
                if telephone_heading and telephone_heading.find_next('p'):
                    telephone = telephone_heading.find_next('p').get_text().strip()

                website_heading = contact_info.find('h3', string='Website')
                if website_heading and website_heading.find_next('p') and website_heading.find_next('p').a:
                    website = website_heading.find_next('p').a.get('href').strip()

                # Scrivi i dettagli nel file CSV
                writer.writerow([trust_name, address, telephone, website])

