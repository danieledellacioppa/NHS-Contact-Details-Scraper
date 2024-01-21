import requests
from bs4 import BeautifulSoup
import csv

# URL della directory del provider NHS
url = "https://www.england.nhs.uk/publication/nhs-provider-directory/"

# Esegui la richiesta HTTP per ottenere il contenuto della pagina
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Trova tutti i link ai Foundation Trusts
trust_links = [link for link in soup.find_all('a', href=True) if 'http' in link['href']]

# Prepara il file CSV per salvare i dettagli di contatto
with open('nhs_contact_details.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Trust Name', 'Address', 'Telephone', 'Website'])  # Intestazioni delle colonne

    for link in trust_links:
        trust_url = link['href']
        trust_response = requests.get(trust_url)
        trust_soup = BeautifulSoup(trust_response.text, 'html.parser')

        # Estrai la sezione dei dettagli di contatto
        contact_section = trust_soup.find('h2', string='Contact details')

        if contact_section:
            contact_info = contact_section.find_next('div', class_='rich-text')

            if contact_info:
                # Estrai il nome del Trust dal tag del titolo, che ha il formato "NHS England » Trust Name"
                title_text = trust_soup.find('title').get_text()
                trust_name = title_text.split('»')[-1].strip() if '»' in title_text else title_text

                print("Extracted Trust Name:", trust_name)

                address_heading = contact_info.find('h3', string='Address')
                address = address_heading.find_next('p').get_text(
                    separator='\n').strip() if address_heading and address_heading.find_next('p') else 'Not found'

                telephone_heading = contact_info.find('h3', string='Telephone')
                telephone = telephone_heading.find_next(
                    'p').get_text().strip() if telephone_heading and telephone_heading.find_next('p') else 'Not found'

                website_heading = contact_info.find('h3', string='Website')
                website = website_heading.find_next('p').a.get(
                    'href').strip() if website_heading and website_heading.find_next('p') and website_heading.find_next(
                    'p').a else 'Not found'

                # Scrivi i dettagli nel file CSV
                writer.writerow([trust_name, address, telephone, website])
        else:
            print(f"Contact details not found for URL: {trust_url}")

print("Scraping completed and data saved to nhs_contact_details.csv")
