"""
    project: project3
    author: Čermák Filip
    email: fifa.allview@gmai.com
    discord: __kys_

    """

import requests
from bs4 import BeautifulSoup
import csv
import argparse

url = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103'

def remove_after_last_slash(url):
    last_slash_index = url.rfind('/')
    if last_slash_index != -1:
        return url[:last_slash_index]
    return url

def postup1(url, output_file):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        
        data = []  

        for row in rows:
            bunky = row.find_all("td")
            if len(bunky) >= 2:
                bunka1 = bunky.pop(0)
                bunka2 = bunky.pop(0)
                links = bunka1.find_all("a") 
                if len(links) >= 1:
                    link1 = links.pop(0)
                    href = link1.get("href")
                    url2 = remove_after_last_slash(url) + "/" + href


                    row_data = [bunka1.get_text(strip=True), bunka2.get_text(strip=True)]

                    krok2(url2, data, row_data)
        
        with open(output_file, 'w', newline='', encoding='cp1250') as file:
            writer = csv.writer(file,delimiter=";")
            writer.writerows(data)
    else:
        print("Chyba při získavání dat")

def krok2(url, excel_rows, row_data):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        hlavicky = []
        
        
        for row in rows:
            bunky = row.find_all("td")
            if len(bunky) == 9:
                bunka1 = bunky.pop(3)
                bunka2 = bunky.pop(3)
                platne_hlasy = bunky.pop(5)
                row_data.extend([bunka1.get_text(strip=True), bunka2.get_text(strip=True), platne_hlasy.get_text(strip=True)])
            elif len(bunky) == 5:
                nazev_strany = bunky.pop(1).get_text(strip=True)
                celkem_hlas = bunky.pop(1).get_text(strip=True)
                row_data.append(celkem_hlas) 
                hlavicky.append(nazev_strany)
        if len(excel_rows) == 0:
            hlavicky = ['code', 'location', 'registered', 'envelopes', 'valid'] + hlavicky
            excel_rows.append(hlavicky)
        excel_rows.append(row_data)
    else:
        print("Chyba při získavání dat")

def main(url, output_file):
    postup1(url, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web scraping script')
    parser.add_argument('url', type=str, help='URL of the website to scrape')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    args = parser.parse_args()
    
    if not args.url or not args.output_file:
        print("Chyba: Musíte zadat oba argumenty: URL a název výstupního souboru.")
    else:
        main(args.url, args.output_file)
