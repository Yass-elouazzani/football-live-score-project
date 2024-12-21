from bs4 import BeautifulSoup
import requests

def botola_standings(url='https://www.lequipe.fr/Football/championnat-du-maroc/page-classement-equipes/general'):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
        return {}

    # Parse the HTML content directly from the response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the standings data
    standings = []
    rows = soup.find_all('tr', class_='table__row')

    for row in rows:
        columns = row.find_all('td')
        if columns:
            team_data = {
                'position': columns[0].text.strip(),
                'team': columns[1].text.strip(),
                'points': columns[3].text.strip(),
                'played': columns[4].text.strip(),
                'won': columns[5].text.strip(),
                'drawn': columns[6].text.strip(),
                'lost': columns[7].text.strip(),
            }
            standings.append(team_data)

    return standings