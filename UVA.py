import streamlit as st
import pandas as pd
import regex as re
import math
import numpy
import seaborn as sns
import pyarrow as pa
import pyarrow.parquet as pq

st.title("UVA Basketball Player Comparison for the 2018-19 season")
st.header("This is an interactive page that allows you to compare two UVA players and their impact based on the lineups they were apart of.")
st.sidebar.title("Streamlit Demo of UVA Basketball Lineup Data")
st.sidebar.write("This page was developed by John Kim and is stored at https://github.com/JohnKim08/UVAStreamlit")
st.sidebar.write("The lineup data was scraped using the R library ncaahoopR https://github.com/lbenz730/ncaahoopR")
df = pd.read_csv("Lineups_separated.csv")

Virginia_players = df.loc[df["Team"] == "Virginia"]
Virginia_players = Virginia_players.drop(columns = ["Unnamed: 0"])
Minimum_playing_time = st.number_input("Minimum number of minutes for a lineup to count")


def grab_roster(df):
    players = []
    df = df.filter(regex=("P\d"))
    for index, row in df.iterrows():
        players.append(row["P1"])
        players.append(row["P2"])
        players.append(row["P3"])
        players.append(row["P4"])
        players.append(row["P5"])
    return list(set(players))
UVA_roster = grab_roster(Virginia_players)
Basketball_ratings = ['Mins', 'oMins',
       'dMins', 'oPOSS', 'dPOSS', 'ORTG', 'DRTG', 'NETRTG', 'PTS', 'dPTS',
       'FGA', 'dFGA', 'FGM', 'dFGM', 'TPA', 'dTPA', 'TPM', 'dTPM', 'FTA',
       'dFTA', 'FTM', 'dFTM', 'RIMA', 'dRIMA', 'RIMM', 'dRIMM', 'ORB', 'dORB',
       'DRB', 'dDRB', 'BLK', 'dBLK', 'TO', 'dTO', 'AST', 'dAST', 'ePOSS',
       'FG.', 'dFG.', 'TPP', 'dTPP', 'FTP', 'dFTP', 'eFG.', 'deFG.', 'TS.',
       'dTS.', 'RIM.', 'dRIM.', 'MID.', 'dMID.', 'TPrate', 'dTPrate',
       'RIMrate', 'dRIMrate', 'MIDrate', 'dMIDrate', 'FTrate', 'dFTrate',
       'ASTrate', 'dASTrate', 'TOrate', 'dTOrate', 'BLKrate', 'oBLKrate',
       'ORB.', 'DRB.', 'TimePerPoss', 'dTimePerPoss']
player_1 = st.selectbox("Pick a player: ", UVA_roster)
player_2 = st.selectbox("Pick a second player: ", UVA_roster)

Category = st.selectbox("Pick a category stat: ", Basketball_ratings )
def find_lineups_with_player(player,df,time):
    data = []
    for index, row in df.iterrows():
        if (player == row["P1"] or player == row["P2"] or player == row["P3"] or player == row["P4"] or player == row["P5"]) and (time < row["Mins"]):
            data.append(row)
    return data
def get_average(category,df):
    return df[category].mean()

player_1_display = find_lineups_with_player(player_1,df,Minimum_playing_time)
player_2_display = find_lineups_with_player(player_2, df, Minimum_playing_time)
player_1_final = pd.DataFrame(player_1_display, columns=['P1', 'P2', 'P3', 'P4', 'P5', 'Team', 'Mins', 'oMins',
       'dMins', 'oPOSS', 'dPOSS', 'ORTG', 'DRTG', 'NETRTG', 'PTS', 'dPTS',
       'FGA', 'dFGA', 'FGM', 'dFGM', 'TPA', 'dTPA', 'TPM', 'dTPM', 'FTA',
       'dFTA', 'FTM', 'dFTM', 'RIMA', 'dRIMA', 'RIMM', 'dRIMM', 'ORB', 'dORB',
       'DRB', 'dDRB', 'BLK', 'dBLK', 'TO', 'dTO', 'AST', 'dAST', 'ePOSS',
       'FG.', 'dFG.', 'TPP', 'dTPP', 'FTP', 'dFTP', 'eFG.', 'deFG.', 'TS.',
       'dTS.', 'RIM.', 'dRIM.', 'MID.', 'dMID.', 'TPrate', 'dTPrate',
       'RIMrate', 'dRIMrate', 'MIDrate', 'dMIDrate', 'FTrate', 'dFTrate',
       'ASTrate', 'dASTrate', 'TOrate', 'dTOrate', 'BLKrate', 'oBLKrate',
       'ORB.', 'DRB.', 'TimePerPoss', 'dTimePerPoss'])
player_2_final = pd.DataFrame(player_2_display, columns=['P1', 'P2', 'P3', 'P4', 'P5', 'Team', 'Mins', 'oMins',
       'dMins', 'oPOSS', 'dPOSS', 'ORTG', 'DRTG', 'NETRTG', 'PTS', 'dPTS',
       'FGA', 'dFGA', 'FGM', 'dFGM', 'TPA', 'dTPA', 'TPM', 'dTPM', 'FTA',
       'dFTA', 'FTM', 'dFTM', 'RIMA', 'dRIMA', 'RIMM', 'dRIMM', 'ORB', 'dORB',
       'DRB', 'dDRB', 'BLK', 'dBLK', 'TO', 'dTO', 'AST', 'dAST', 'ePOSS',
       'FG.', 'dFG.', 'TPP', 'dTPP', 'FTP', 'dFTP', 'eFG.', 'deFG.', 'TS.',
       'dTS.', 'RIM.', 'dRIM.', 'MID.', 'dMID.', 'TPrate', 'dTPrate',
       'RIMrate', 'dRIMrate', 'MIDrate', 'dMIDrate', 'FTrate', 'dFTrate',
       'ASTrate', 'dASTrate', 'TOrate', 'dTOrate', 'BLKrate', 'oBLKrate',
       'ORB.', 'DRB.', 'TimePerPoss', 'dTimePerPoss'])


player_1_number = get_average(Category, player_1_final)
# st.text(f"AVERAGE {str(Category)}:  " +str(player_1_number))
st.subheader(f"{player_1} Lineups ")
st.dataframe(player_1_final)
player_2_number = get_average(Category, player_2_final)
# st.text(f"AVERAGE {str(Category)}:  " +str(player_2_number))
st.subheader(f"{player_2} Lineups ")
st.dataframe(player_2_final)

## Graph final
final_graph_data = ({ "Names": [f"{player_1}",f"{player_2}"], f"Average: {Category}": [player_1_number,player_2_number]})
final_df = pd.DataFrame(final_graph_data,columns=["Names",f"Average: {Category}"])
final_df = final_df.set_index("Names")
# st.dataframe(final_df)

st.bar_chart(final_df[f"Average: {Category}"])
