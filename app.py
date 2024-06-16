from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import json
import pandas as pd
from datetime import datetime


app = Flask(__name__)
CORS(app)


def get_last_10_perf(team, data):
    nb_games="10"
    df_last_10_games = data[data['teamTricode'] == team].tail(10)
    #df_last_10_games
    df_stat_last_perf = pd.DataFrame(columns=['NB_WIN_L10', 'PCT_TIR_REUSSI_L10','PCT_3PTS_L10', 
                               'PCT_LANCER_FRANC_L10','estimatedOffensiveRating_L10', 'offensiveRating_L10',
                               'estimatedDefensiveRating_L10',
                               'defensiveRating_L10','estimatedNetRating_L10', 'netRating_L10', 'assistPercentage_L10',
                               'assistToTurnover_L10', 'assistRatio_L10','estimatedTeamTurnoverPercentage_L10', 'turnoverRatio_L10',
                               'effectiveFieldGoalPercentage_L10','trueShootingPercentage_L10', 'estimatedPace_L10', 'pace_L10',
                               'pacePer40_L10', 'PIE_L10'])
    df_last_10_games.reset_index(drop=True, inplace=True)
    new_row = {"NB_WIN_L"+nb_games : (df_last_10_games['WL'] == 'W').sum() / int(nb_games),
                       "PCT_TIR_REUSSI_L"+nb_games : df_last_10_games['PCT_TIR_REUSSI'].mean(),
                       "PCT_3PTS_L"+nb_games : df_last_10_games['PCT_3PTS'].mean(),
                       "PCT_LANCER_FRANC_L"+nb_games : df_last_10_games['PCT_LANCER_FRANC'].mean(),
                       "estimatedOffensiveRating_L"+nb_games : df_last_10_games['estimatedOffensiveRating'].mean(),
                       "offensiveRating_L"+nb_games : df_last_10_games['offensiveRating'].mean(),
                       "estimatedDefensiveRating_L"+nb_games : df_last_10_games['estimatedDefensiveRating'].mean(),
                       "defensiveRating_L"+nb_games : df_last_10_games['defensiveRating'].mean(),
                       "estimatedNetRating_L"+nb_games : df_last_10_games['estimatedNetRating'].mean(),
                       "netRating_L"+nb_games : df_last_10_games['netRating'].mean(),
                       "assistPercentage_L"+nb_games : df_last_10_games['assistPercentage'].mean(),
                       "assistToTurnover_L"+nb_games : df_last_10_games['assistToTurnover'].mean(),
                       "assistRatio_L"+nb_games : df_last_10_games['assistRatio'].mean(),
                       "estimatedTeamTurnoverPercentage_L"+nb_games : df_last_10_games['estimatedTeamTurnoverPercentage'].mean(),
                       "turnoverRatio_L"+nb_games : df_last_10_games['turnoverRatio'].mean(),
                       "effectiveFieldGoalPercentage_L"+nb_games : df_last_10_games['effectiveFieldGoalPercentage'].mean(),
                       "trueShootingPercentage_L"+nb_games : df_last_10_games['trueShootingPercentage'].mean(),
                       "estimatedPace_L"+nb_games : df_last_10_games['estimatedPace'].mean(),
                       "pace_L"+nb_games : df_last_10_games['pace'].mean(),
                       "pacePer40_L"+nb_games : df_last_10_games['pacePer40'].mean(),
                       "PIE_L"+nb_games : df_last_10_games['PIE'].mean()}
    df_stat_last_perf.loc[len(df_stat_last_perf)] = new_row
    return df_stat_last_perf

def get_elo(team_name, data_elo):
    df_elo_home = data_elo[data_elo['team1'] == team_name]
    df_elo_away = data_elo[data_elo['team2'] == team_name]
    
    if datetime.strptime(df_elo_home['date'].iloc[-1], '%Y-%m-%d') > datetime.strptime(df_elo_away['date'].iloc[-1], '%Y-%m-%d'):
        return df_elo_home['elo1_post'].iloc[-1]
    else :
        return df_elo_away['elo2_post'].iloc[-1]

def get_prediction(home_team, away_team):
    with open('team_name.json', 'r') as file:
        team_dict = json.load(file)
        
    data = pd.read_csv("dataset.csv", dtype={'teamId' : str})
    data_elo = pd.read_csv("nba_elo.csv", dtype={'teamId' : str})
    data_elo['team1'] = data_elo['team1'].replace({'PHO': 'PHX', 'BRK': 'BKN', 'CHO': 'CHA'})
    data_elo['team2'] = data_elo['team2'].replace({'PHO': 'PHX', 'BRK': 'BKN', 'CHO': 'CHA'})
    data_elo['team1'] = data_elo['team1'].replace(team_dict)
    data_elo['team2'] = data_elo['team2'].replace(team_dict)
    data['teamTricode'] = data['teamTricode'].replace(team_dict)
    # Charger le contenu du fichier JSON dans un dictionnaire
    
        
    stat_home = get_last_10_perf(home_team, data)
    stat_home['ELO'] = get_elo(home_team, data_elo)
    stat_away = get_last_10_perf(away_team, data)
    stat_away['ELO'] = get_elo(away_team, data_elo)
    
    stat = []
    for column in stat_home.columns :
        stat.append(stat_home[column].iloc[-1] - stat_away[column].iloc[-1])
    data = {colonne: [valeur] for colonne, valeur in zip(stat_home.columns.tolist(), stat)}
    df = pd.DataFrame(data)
    df.drop(columns=['NB_WIN_L10','PCT_TIR_REUSSI_L10', 'PCT_3PTS_L10', 'effectiveFieldGoalPercentage_L10','trueShootingPercentage_L10'])

    new_order = ['ELO', 'PCT_LANCER_FRANC_L10', 'PIE_L10', 'assistPercentage_L10',
       'assistRatio_L10', 'assistToTurnover_L10', 'defensiveRating_L10',
       'estimatedDefensiveRating_L10', 'estimatedNetRating_L10',
       'estimatedOffensiveRating_L10', 'estimatedPace_L10',
       'estimatedTeamTurnoverPercentage_L10', 'netRating_L10',
       'offensiveRating_L10', 'pacePer40_L10', 'pace_L10',
       'turnoverRatio_L10']
    df = df.reindex(columns=new_order)
    
    # Charger le modèle et le scaler sauvegardés
    model = joblib.load('KNN.pkl')
    scaler = joblib.load('scaler.pkl')
    
    # Transformer les nouvelles données avec le scaler chargé
    X_new_scaled = scaler.transform(df)
    
    # Faire des prédictions avec le modèle chargé
    predictions = model.predict(X_new_scaled)
    if predictions[0] == 1:
        return home_team
    else:
        return away_team
    

#get_prediction("Los Angeles Lakers", "San Antonio Spurs")


@app.route('/api/get_prediction', methods=['POST'])
def get_winner():
    data = request.json
    home_team = data.get('num1')
    away_team = data.get('num2')
    winner = get_prediction(home_team, away_team)
    return jsonify({'result': winner})

@app.route('/')
def serve_index():
    return send_from_directory('.', 'html.html')

@app.route('/test')
def serve_test():
    return send_from_directory('.', 'test.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
