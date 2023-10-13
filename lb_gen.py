import requests
from datetime import datetime
from random import randint

api_key = "API KEY HERE"
lowest_winstreak = "100"
lowest_other_queries = "100"
query_types = ["winstreak", "max_possible_winstreak","fkdr", "wlr", "bblr"]
game_types = ["overall", "eight_one", "eight_two", "four_three", "four_four", "two_four"]

filename = "leaderboard.txt"
stats_api_url = "https://api.antisniper.net/v2/resources/stats?key={}".format(api_key)
response = requests.get(stats_api_url)
if response.status_code == 200:
    data = response.json()
    uuid_list_length = data["uuid_list"]
else:
    print("API request failed with status code:", response.status_code)

with open(filename, "w") as f:
    uuid_list_text = f"{uuid_list_length/1000000:,.0f} million"

    intro_text = f"The method I use to generate the leaderboard is based on an ever growing {uuid_list_text} uuid list." \
                 " There are no ways to bypass my method so this will be 100% perfect. I will try to update it daily." \
                 "This is raw data so there will be hackers / boosters on here however please do not publicly call them" \
                 " out in this thread. Enjoy!!!!"
    title_text = f"Ongoing Leaderboard - Updated {datetime.now().strftime('%d-%B')}"

    sal_text = f"To view all-time Winstreak Records Leaderboard Please Visit [URL='https://hypixel.net/threads/official-highest-bedwars-winstreaks-leaderboard.1979412']Sal's thread[/URL]:"
    f.write(f"[CENTER][SIZE=7][B][U][COLOR=rgb(184, 49, 47)]{title_text}[/COLOR][/U][/B][/SIZE][/CENTER]\n")
    f.write(f"[CENTER][SIZE=4]{intro_text}[/SIZE]\n\n[SIZE=5]{sal_text}[/SIZE][/CENTER]\n\n")
    for game_type in game_types:
        f.write(f"[CENTER][SIZE=7][B][COLOR=rgb({randint(0, 256)}, {randint(0, 256)}, {randint(0, 256)})]{game_type.replace('_', ' ').capitalize()}[/COLOR][/B][/SIZE][/CENTER]\n")
        for query_type in query_types:
            query_type_prefixed = f"{game_type}_{query_type}"
            if game_type in ["overall", "eight_two"] and query_type == "fkdr":
                lowest = "250"
            else:
                lowest = "100"
            api_url = f"https://api.antisniper.net/v2/leaderboard/classic?key={api_key}&mode={game_type}&stat={query_type}&lowest={lowest}"

            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()["data"]
                formatted_query_type = query_type.replace("_", " ").capitalize()
                f.write(f"[CENTER][SPOILER=\"{formatted_query_type}\"]")
                for i, player in enumerate(data):
                    if i >= 150:
                        break
                    ign = player["ign"]
                    value = player[query_type_prefixed]
                    f.write(f"{i+1}: {ign} {value}\n")
                f.write(f"[/SPOILER][/CENTER]\n")
            else:
                print("API request failed with status code:", response.status_code)


