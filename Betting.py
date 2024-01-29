import requests
from datetime import datetime

def get_player_id(player_name):
    response = requests.get(f"https://www.balldontlie.io/api/v1/players?search={player_name}")
    players = response.json()['data']
    if players:
        return players[0]['id']  # Return ID of the first match
    else:
        return None

def get_current_season():
    current_year = datetime.now().year
    current_month = datetime.now().month
    # The NBA season starts in October; before October, subtract 1 from the current year
    season_year = current_year if current_month >= 10 else current_year - 1
    return season_year

def get_recent_games(player_id, num_games):
    season_year = get_current_season()
    response = requests.get(f"https://www.balldontlie.io/api/v1/stats?seasons[]={season_year}&player_ids[]={player_id}&per_page=100")
    games = response.json()['data']
    # Sort games by date in descending order and pick the last 'num_games' games
    sorted_games = sorted(games, key=lambda x: datetime.strptime(x['game']['date'], '%Y-%m-%dT%H:%M:%S.%fZ'), reverse=True)
    return sorted_games[:num_games]

def calculate_probability(games, stat, benchmark):
    count = sum(1 for game in games if game[stat] > benchmark)
    return count / len(games) if games else 0

def main():
    player_name = input("Enter player name (e.g., 'Stephen Curry'): ")
    stat = input("Enter the stat to check (e.g., 'pts', 'ast', 'reb'): ")
    benchmark = int(input(f"Enter the benchmark for {stat} (e.g., 30 for points): "))
    num_games = 5  # Analyze the last 5 games

    player_id = get_player_id(player_name)
    if player_id:
        games = get_recent_games(player_id, num_games)
        probability = calculate_probability(games, stat, benchmark)
        print(f"Probability of {player_name} achieving over {benchmark} {stat}: {probability:.2f}")
    else:
        print("Player not found. Please check the name and try again.")

if __name__ == "__main__":
    main()

