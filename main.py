from bs4 import BeautifulSoup
import requests
import pandas as pd
import exceptions
import math

def extract_job_description(all_descriptions):
    text = ''

    for i in all_descriptions:
        text += i.text.strip()

    return text

def extracts_jobs_info(jobs_cards):
    
    data = []

    for job_card in jobs_cards:
        data.append({
            'title'    : job_card.find('div', {'class':'css-pkv5jc'}).find('div', {'class':'css-laomuu'}).find('h2').text.strip(),
            'location' : job_card.find('div', {'class':'css-pkv5jc'}).find('div', {'class':'css-laomuu'}).find('div', {'class' : 'css-d7j1kk'}).find('span').text.strip(),
            'link'     : job_card.find('div', {'class':'css-pkv5jc'}).find('div', {'class':'css-laomuu'}).find('div', {'class' : 'css-d7j1kk'}).find('a').get('href'),
            'from'     : job_card.find('div', {'class':'css-pkv5jc'}).find('div', {'class':'css-laomuu'}).find('div', {'class' : 'css-d7j1kk'}).find('div').text.strip(),
            'type'     : job_card.find('div', {'class':'css-pkv5jc'}).find('div', {'class':'css-y4udm8'}).contents[0].contents[0].text.strip(),
            'disc'     : extract_job_description(job_card.find('div', {'class':'css-pkv5jc'}).find('div', {'class':'css-y4udm8'}).find_all('a', {'class' : 'css-o171kl'}))
        })
        
    return data

def get_number_of_pages(page):
    
    soup = BeautifulSoup(page.content, 'lxml')
    search_result = soup.find('span', {'class' : 'css-xkh9ud'}).find("strong").text.strip()
    pages_number = range(0, math.ceil(int(search_result)/15))

    print(f"{len(pages_number)} page extracting now.")

    return len(pages_number)


def main(query_search):
    
    print('Please wait, that will might take a few seconds....')

    page = requests.get(f"https://wuzzuf.net/search/jobs/?q={query_search}")
    df = pd.DataFrame()
    pages_list = [i for i in range(0, get_number_of_pages(page))]

    for start in pages_list:

        page = requests.get(f"https://wuzzuf.net/search/jobs/?q={query_search}&start={start}")
        soup = BeautifulSoup(page.content, 'lxml')
        jobs_cards = soup.find_all('div', {'class': 'css-1gatmva'})
        data = extracts_jobs_info(jobs_cards)
        
        if data: 
            df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    if not df.empty:
        df.to_excel('data.xlsx', index=False)
        print('Extracting done successfully.')
    else:
        print("No job data found.")


query_search = input('Search about jobs: ')

main(query_search)