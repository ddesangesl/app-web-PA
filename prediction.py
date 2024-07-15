import joblib
import json
import pandas as pd
from datetime import datetime

def get_last_10_perf(team, data):
    nb_games="10"
    df_last_10_games = data[data['teamTricode'] == team].tail(10)

    # Définition des colonne de la dataframe contenant la moyenne des 10 derniere performance des deux équipe  avant le match
    df_stat_last_perf = pd.DataFrame(
        columns=[ 'NB_WIN_L' + nb_games, "AVG_POINTS" + nb_games,
                 'PCT_TIR_REUSSI_L' + nb_games, 'PCT_3PTS_L' + nb_games,
                 'PCT_LANCER_FRANC_L' + nb_games, "PASSE_D_L" + nb_games, "REBOND" + nb_games,
                 "REBOND_OFF" + nb_games, "REBOND_DEF" + nb_games, "INTERCEPTIONS_L" + nb_games,
                 "TIR_CONTREE" + nb_games, "BALLON_PERDU_L" + nb_games, "FAUTES_L" + nb_games,
                 'estimatedOffensiveRating_L' + nb_games, 'offensiveRating_L' + nb_games,
                 'estimatedDefensiveRating_L' + nb_games,
                 'defensiveRating_L' + nb_games, 'estimatedNetRating_L' + nb_games, 'netRating_L' + nb_games,
                 'assistPercentage_L' + nb_games,
                 'assistToTurnover_L' + nb_games, 'assistRatio_L' + nb_games,
                 'estimatedTeamTurnoverPercentage_L' + nb_games, 'turnoverRatio_L' + nb_games,
                 'effectiveFieldGoalPercentage_L' + nb_games, 'trueShootingPercentage_L' + nb_games,
                 'estimatedPace_L' + nb_games, 'pace_L' + nb_games,
                 'pacePer40_L' + nb_games, 'PIE_L' + nb_games, "offensiveReboundPercentage_L" + nb_games,
                 "defensiveReboundPercentage_L" + nb_games, "reboundPercentage_L" + nb_games,
                 "estimatedUsagePercentage_L" + nb_games, "possesions_L" + nb_games])
    df_last_10_games.reset_index(drop=True, inplace=True)

    # Crée une ligne contenant les moyenne des stats des 10 dernier performance d'une équipe le match
    new_row = {"NB_WIN_L" + nb_games: (df_last_10_games['WL'] == 'W').sum() / int(nb_games),
                       "AVG_POINTS" + nb_games: df_last_10_games['TOTAL_POINTS'].mean(),
                       "PCT_TIR_REUSSI_L" + nb_games: df_last_10_games['PCT_TIR_REUSSI'].mean(),
                       "PCT_3PTS_L" + nb_games: df_last_10_games['PCT_3PTS'].mean(),
                       "PCT_LANCER_FRANC_L" + nb_games: df_last_10_games['PCT_LANCER_FRANC'].mean(),
                       "PASSE_D_L" + nb_games: df_last_10_games['PASSE_D'].mean(),
                       "REBOND" + nb_games: df_last_10_games['REBOND'].mean(),
                       "REBOND_OFF" + nb_games: df_last_10_games['REBOND_OFF'].mean(),
                       "REBOND_DEF" + nb_games: df_last_10_games['REBOND_DEF'].mean(),
                       "INTERCEPTIONS_L" + nb_games: df_last_10_games['INTERCEPTION'].mean(),
                       "TIR_CONTREE" + nb_games: df_last_10_games['TIR_CONTRE'].mean(),
                       "BALLON_PERDU_L" + nb_games: df_last_10_games['BALLON_PERDU'].mean(),
                       "FAUTES_L" + nb_games: df_last_10_games['FAUTES'].mean(),
                       "estimatedOffensiveRating_L" + nb_games: df_last_10_games['estimatedOffensiveRating'].mean(),
                       "offensiveRating_L" + nb_games: df_last_10_games['offensiveRating'].mean(),
                       "estimatedDefensiveRating_L" + nb_games: df_last_10_games['estimatedDefensiveRating'].mean(),
                       "defensiveRating_L" + nb_games: df_last_10_games['defensiveRating'].mean(),
                       "estimatedNetRating_L" + nb_games: df_last_10_games['estimatedNetRating'].mean(),
                       "netRating_L" + nb_games: df_last_10_games['netRating'].mean(),
                       "assistPercentage_L" + nb_games: df_last_10_games['assistPercentage'].mean(),
                       "assistToTurnover_L" + nb_games: df_last_10_games['assistToTurnover'].mean(),
                       "assistRatio_L" + nb_games: df_last_10_games['assistRatio'].mean(),
                       "offensiveReboundPercentage_L" + nb_games: df_last_10_games['offensiveReboundPercentage'].mean(),
                       "defensiveReboundPercentage_L" + nb_games: df_last_10_games['defensiveReboundPercentage'].mean(),
                       "reboundPercentage_L" + nb_games: df_last_10_games['reboundPercentage'].mean(),
                       "estimatedTeamTurnoverPercentage_L" + nb_games: df_last_10_games['estimatedTeamTurnoverPercentage'].mean(),
                       "turnoverRatio_L" + nb_games: df_last_10_games['turnoverRatio'].mean(),
                       "effectiveFieldGoalPercentage_L" + nb_games: df_last_10_games['effectiveFieldGoalPercentage'].mean(),
                       "trueShootingPercentage_L" + nb_games: df_last_10_games['trueShootingPercentage'].mean(),
                       "estimatedUsagePercentage_L" + nb_games: df_last_10_games['estimatedUsagePercentage'].mean(),
                       "estimatedPace_L" + nb_games: df_last_10_games['estimatedPace'].mean(),
                       "pace_L" + nb_games: df_last_10_games['pace'].mean(),
                       "pacePer40_L" + nb_games: df_last_10_games['pacePer40'].mean(),
                       "possessions_L" + nb_games: df_last_10_games['possessions'].mean(),
                       "PIE_L" + nb_games: df_last_10_games['PIE'].mean()}
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
    
    # Recupere les 10 derniere performance et le dernier score ELO des 2 equipes    
    stat_home = get_last_10_perf(home_team, data)
    stat_home['ELO'] = get_elo(home_team, data_elo)
    stat_away = get_last_10_perf(away_team, data)
    stat_away['ELO'] = get_elo(away_team, data_elo)
    
    stat = []
    
    # Fait la difference des statistique entre l'equipe a domicile et l'equipe a l'exterieur
    for column in stat_home.columns :
        stat.append(stat_home[column].iloc[-1] - stat_away[column].iloc[-1])

    data = {colonne: [valeur] for colonne, valeur in zip(stat_home.columns.tolist(), stat)}
    df = pd.DataFrame(data)
    df.drop(columns=['estimatedUsagePercentage_L10', 'trueShootingPercentage_L10', 'effectiveFieldGoalPercentage_L10', 'reboundPercentage_L10', 'NB_WIN_L10', 'PCT_TIR_REUSSI_L10', 'PIE_L10', 'PCT_3PTS_L10', 'PCT_LANCER_FRANC_L10', 'pace_L10' ])

    new_order = [ 'ELO', 'BALLON_PERDU_L10', 'AVG_POINTS10',
       'INTERCEPTIONS_L10', 'PASSE_D_L10', 'REBOND_DEF10',
       'REBOND10', 'REBOND_OFF10', 'TIR_CONTREE10', 'assistPercentage_L10',
       'assistRatio_L10', 'assistToTurnover_L10', 'defensiveRating_L10',
       'defensiveReboundPercentage_L10', 'estimatedDefensiveRating_L10',
       'estimatedNetRating_L10', 'estimatedOffensiveRating_L10',
       'estimatedPace_L10', 'estimatedTeamTurnoverPercentage_L10',
       'netRating_L10', 'offensiveRating_L10', 'pacePer40_L10',
       'offensiveReboundPercentage_L10', 'turnoverRatio_L10']
    df = df.reindex(columns=new_order)
    
    # Charge le modèle et le scaler sauvegardés
    model = joblib.load('GB.pkl')
    scaler = joblib.load('GB_scaler.pkl')
    
    # Transforme les nouvelles données avec le scaler chargé
    X_new_scaled = scaler.transform(df)
    
    # Fait des prédictions avec le modèle chargé
    predictions = model.predict(X_new_scaled)
    if predictions[0] == 1:
        return home_team
    else:
        return away_team