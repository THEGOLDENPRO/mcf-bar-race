import csv
import pandas as pd
import bar_chart_race as bcr
from devgoldyutils import Colours
from novauniverse import MCF, TournamentPlayer
from typing import Dict

mcf = MCF()

print(Colours.ORANGE.apply_to_string("Getting all mcf data..."))
all_mcfs = mcf.get_all()

print(Colours.BLUE.apply_to_string("Getting information on top mcf players..."))
relevant_players = [player for player in mcf.get_top_players(max_players = 9999)]

score_count:Dict[str, TournamentPlayer] = {}

for player in relevant_players:
    player.score = 0 # Zero all scores.
    score_count[player.uuid] = player

with open("./temp.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Date"] + [player.name for player in relevant_players])
    
    for mcf in all_mcfs:
        player_scores = []

        for relevant_player_uuid in score_count:
            player_found = False

            for player in mcf.players:

                if player.uuid == relevant_player_uuid:
                    player_found = True
                    score_count[relevant_player_uuid].score += player.score
                    player_scores.append(
                        score_count[relevant_player_uuid].score
                    )

                    break
            
            if not player_found:
                player_scores.append(score_count[relevant_player_uuid].score)

        writer.writerow([mcf.display_name] + player_scores)
        print(Colours.GREEN.apply_to_string(f"Done mcf '{mcf.display_name}'."))


# Generate bar chart race
# -------------------------
df = pd.read_csv("./temp.csv", index_col="Date")

print(Colours.PINK_GREY.apply_to_string("Generating bar chart race..."))
bcr.bar_chart_race(
    df = df,
    bar_label_size = 19,
    tick_label_size = 20,
    steps_per_period = 30,
    period_length = 1000,
    filename = 'video3.mp4',
    figsize = (18, 10.5)
)