import requests

def get_player_id(player_name):
    response = requests.get(f"https://www.balldontlie.io/api/v1/players?search={player_name}")
    players = response.json()['data']
    if players:
        return players[0]['id']  # Return ID of the first match
    else:
        return None

def get_recent_games(player_id, num_games):
    response = requests.get(f"https://www.balldontlie.io/api/v1/stats?player_ids[]={player_id}&per_page={num_games}")
    games = response.json()['data']
    print("Games data fetched:", games)  # Print the games data
    return games

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
