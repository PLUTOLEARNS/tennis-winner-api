import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://en.wikipedia.org/wiki/List_of_Wimbledon_gentlemen%27s_singles_champions"

response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.content, 'html.parser')

tables = soup.find_all('table', {'class': 'sortable wikitable'})

print(f"Found {len(tables)} tables on the page")

def extract_data_from_table(table, table_name=""):
    data = []
    rows = table.find_all('tr')[1:]
    print(f"Processing {table_name} with {len(rows)} rows")
    
    for i, row in enumerate(rows):
        cells = row.find_all('td')
        if len(cells) >= 6:
            year_text = cells[0].text.strip()
            if re.match(r'^\d{4}', year_text):
                year = int(year_text)
                
                champion = ""
                runner_up = ""
                
                champion_span = cells[2].find('span', {'class': 'fn'})
                runner_up_span = cells[4].find('span', {'class': 'fn'})
                
                if champion_span and runner_up_span:
                    champion = champion_span.text.strip()
                    runner_up = runner_up_span.text.strip()
                else:
                    champion_link = cells[2].find('a')
                    runner_up_link = cells[4].find('a')
                    
                    if champion_link:
                        champion = champion_link.text.strip()
                    else:
                        champion = cells[2].text.strip()
                    
                    if runner_up_link:
                        runner_up = runner_up_link.text.strip()
                    else:
                        runner_up = cells[4].text.strip()
                
                if champion and runner_up:
                    score = cells[5].text.strip()
                    score = score.replace('–', '-').replace('—', '-').replace('â€"', '-')
                    sets, tiebreak = calculate_sets_and_tiebreak(score)
                    data.append([year, champion, runner_up, score, sets, tiebreak])
                    print(f"  Added: {year} - {champion} vs {runner_up}")
    
    return data

def calculate_sets_and_tiebreak(score):
    if "walkover" in score.lower() or "w.o." in score.lower():
        return 1, 0
    
    score_clean = re.split(r'retired|walkover|w\.o\.', score, flags=re.IGNORECASE)[0].strip()
    
    parts = [p.strip() for p in score_clean.split(',') if p.strip()]
    
    valid_parts = []
    for part in parts:
        if re.search(r'\d+[-–]\d+', part):
            valid_parts.append(part)
    
    sets = len(valid_parts)
    
    tiebreak = 1 if any(re.search(r'\(\d+[-–]\d+\)', part) for part in valid_parts) else 0
    
    return max(sets, 1), tiebreak

all_data = []

for i, table in enumerate(tables):
    print(f"\n--- Processing Table {i+1} ---")
    
    headers = table.find('tr')
    if headers:
        header_text = headers.text.lower()
        print(f"Table headers: {header_text[:100]}...")
    
    table_data = extract_data_from_table(table, f"Table {i+1}")
    
    if table_data:
        all_data.extend(table_data)
        print(f"Added {len(table_data)} records from Table {i+1}")
    else:
        print(f"No valid data found in Table {i+1}")

if all_data:
    df_combined = pd.DataFrame(all_data, columns=["year", "champion", "runner_up", "score", "sets", "tiebreak"])
    
    df_combined = df_combined.sort_values('year').drop_duplicates(subset=['year'], keep='first')
    
    df_combined.to_csv('wimbledon_finals.csv', index=False)
    
    print(f"\nData scraped successfully!")
    print(f"Total records: {len(df_combined)}")
    print(f"Year range: {df_combined['year'].min()} - {df_combined['year'].max()}")
    print(f"First few records:")
    print(df_combined.head())
    print(f"\nData saved to 'wimbledon_finals.csv'")
else:
    print("No data was extracted. Please check the table structure.")