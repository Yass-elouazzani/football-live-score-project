import requests
import pytz
from datetime import datetime, timedelta
from colorama import Fore, Style, init
from parse_standings import botola_standings
from dotenv import load_dotenv
import os
from requests.exceptions import RequestException

load_dotenv()

# colorama
init(autoreset=True)

# API token
API_TOKEN = os.getenv('API_TOKEN')
BASE_URL = 'https://api.football-data.org/v2/'

HEADERS = {
    'X-Auth-Token': API_TOKEN
}

# available competitions
competitions = {
    '1': ('UEFA Champions League', 'CL'),
    '2': ('Ligue 1', 'FL1'),
    '3': ('La Liga', 'PD'),
    '4': ('Premier League', 'PL'),
    '5': ('Serie A', 'SA'),
    '6': ('Bundesliga', 'BL1'),
    '7': ('Primeira Liga', 'PPL'),
    '8': ('Serie A (Brazil)', 'BSA'),
}

def fetch_data(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(Fore.RED + f"Error fetching data: {e}" + Style.RESET_ALL)
        return None

def display_menu():
    print(f"{Style.BRIGHT}{Fore.LIGHTRED_EX}Choose a competition:")
    for key, (name, code) in competitions.items():
        print(f"{Style.BRIGHT}{Fore.CYAN}{key}{Style.RESET_ALL}. {name}")
    print(f'{Style.BRIGHT}{Fore.CYAN}9{Style.RESET_ALL}. Botola Pro')
    print(f'{Style.BRIGHT}{Fore.CYAN}0{Style.RESET_ALL}.{Style.RESET_ALL} Exit')

def display_botola_standings():
    print(f'{Style.BRIGHT}{Fore.MAGENTA}Standings for Botola Pro{Style.RESET_ALL}')
    standings = botola_standings()
    for index, team in enumerate(standings, start=1):
        print(f"{Style.BRIGHT}{Fore.CYAN}{index}{Style.RESET_ALL}. {team['team']} - Points: {team['points']}, Played: {team['played']}, Won: {team['won']}, Drawn: {team['drawn']}, Lost: {team['lost']}")
    print()

def handle_botola_pro():
    print(f"{Style.BRIGHT}{Fore.LIGHTRED_EX}Choose the type of information for Botola Pro:")
    print(f"{Style.BRIGHT}{Fore.CYAN}1{Style.RESET_ALL}. Standings")
    # Add more options here in the future

    botola_choice = input(f"{Style.BRIGHT}{Fore.LIGHTRED_EX}Enter the number of your choice: {Style.RESET_ALL}")
    print()

    if botola_choice == '1':
        display_botola_standings()
    else:
        print("Invalid choice. Please try again.")

def get_competition_info(competition_code, info_choice):
    today_date = datetime.today().strftime('%Y-%m-%d')
    tomorrow_date = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    next_month_date = (datetime.now() + timedelta(30)).strftime('%Y-%m-%d')

    if info_choice == '1':
        url = f'https://api.football-data.org/v4/competitions/{competition_code}/matches?dateFrom={today_date}&dateTo={today_date}'
    elif info_choice == '2':
        url = f'https://api.football-data.org/v4/competitions/{competition_code}/matches?dateFrom={today_date}&dateTo={next_month_date}'
    elif info_choice == '3':
        url = f'https://api.football-data.org/v4/competitions/{competition_code}/matches?dateFrom={tomorrow_date}&dateTo={tomorrow_date}'
    elif info_choice == '4':
        url = f'https://api.football-data.org/v4/competitions/{competition_code}/standings'
    else:
        print("Invalid choice. Please try again.")
        return None

    return fetch_data(url)

def display_competition_info(competition_name, data, info_choice):
    if info_choice == '4':
        print(f"{Style.BRIGHT}{Fore.MAGENTA}Standings for {competition_name}")
        standings = data.get('standings', [])
        if not standings:
            print("No standings available.")
        else:
            for standing in standings:
                table = standing.get('table', [])
                for team in table:
                    print(f"{team['position']}. {team['team']['name']} - Points: {team['points']}")
        print()
    else:
        print(f"{Fore.LIGHTMAGENTA_EX}Competition: {competition_name}")
        rabat_tz = pytz.timezone('Africa/Casablanca')
        matches = data.get('matches', [])
        if not matches:
            print("There are no matches scheduled for this date.")
        else:
            for match in matches:
                home_team = match['homeTeam']['name']
                away_team = match['awayTeam']['name']
                match_time_utc = match['utcDate']
                match_time = datetime.strptime(match_time_utc, '%Y-%m-%dT%H:%M:%SZ')
                match_time = match_time.replace(tzinfo=pytz.utc).astimezone(rabat_tz)
                match_time_str = match_time.strftime('%Y-%m-%d %H:%M:%S %Z')
                score = match.get('score', {})
                full_time = score.get('fullTime', {})
                home_score = full_time.get('home', 'N/A')
                away_score = full_time.get('away', 'N/A')
                status = match.get('status', 'N/A')
                print(f"Match: {Fore.CYAN}{home_team}{Style.RESET_ALL} vs {Fore.CYAN}{away_team}")
                print(f"Time: {match_time_str}")
                print(f"Score: {home_score} - {away_score}")
                print(f"Status: {status}")
                print()

def main():
    while True:
        display_menu()
        competition_choice = input(f"{Style.BRIGHT}{Fore.LIGHTRED_EX}Enter the number of your choice: {Style.RESET_ALL}")
        print()

        if competition_choice == '9':
            handle_botola_pro()
            continue
        elif competition_choice == '0':
            print("Exiting the program.")
            break

        competition_name, competition_code = competitions.get(competition_choice, ('Unknown Competition', ''))
        print(f"{Style.BRIGHT}{Fore.LIGHTRED_EX}Choose the type of information:")
        print(f"{Style.BRIGHT}{Fore.CYAN}1{Style.RESET_ALL}. Today's matches")
        print(f"{Style.BRIGHT}{Fore.CYAN}2{Style.RESET_ALL}. All scheduled matches")
        print(f"{Style.BRIGHT}{Fore.CYAN}3{Style.RESET_ALL}. Tomorrow’s matches")
        print(f"{Style.BRIGHT}{Fore.CYAN}4{Style.RESET_ALL}. Standings")

        info_choice = input(f"{Style.BRIGHT}{Fore.LIGHTRED_EX}Enter the number of your choice: {Style.RESET_ALL}")
        print()
        data = get_competition_info(competition_code, info_choice)
        if data:
            display_competition_info(competition_name, data, info_choice)

if __name__ == "__main__":
    main()