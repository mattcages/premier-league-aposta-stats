import os
import json
import re
from datetime import datetime

def clean_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")

def charger_stats_club(nom_club):
    """Charge les stats d'un club depuis son fichier"""
    root = "Premier_League_2526"
    chemin = os.path.join(root, "Clubs", clean_name(nom_club), "stats_club.txt")
    
    if not os.path.exists(chemin):
        print(f"⚠️ Fichier stats manquant pour {nom_club}")
        return None

    stats = {}
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
        
    # Extraire les données avec regex
    lignes = contenu.split('\n')
    for ligne in lignes:
        if ':' in ligne and not ligne.startswith(('=', '📊', '🏆', '🆔')):
            nom, valeur = ligne.split(':', 1)
            nom_propre = re.sub(r'\s+', '', nom.lower())  # Enlève espaces
            try:
                valeur = float(valeur.strip())
                stats[nom_propre] = valeur
            except ValueError:
                # Garder les chaînes comme IDs
                stats[nom_propre] = valeur.strip()
    
    # Renommer pour correspondre aux programmes
    mapping = {
        'accuratecrosses': 'Accurate crosses',
        'accuratecrossespercentage': 'Accurate crosses percentage',
        'accuratefinalthirdpassesagainst': 'Accurate final third passes against',
        'accuratelongballs': 'Accurate long balls',
        'accuratelongballspercentage': 'Accurate long balls percentage',
        'accurateoppositionhalfpasses': 'Accurate opposition half passes',
        'accurateoppositionhalfpassespercentage': 'Accurate opposition half passes percentage',
        'accurateownhalfpasses': 'Accurate own half passes',
        'accurateownhalfpassespercentage': 'Accurate own half passes percentage',
        'accuratepasses': 'Accurate passes',
        'accuratepassespercentage': 'Accurate passes percentage',
        'aerialduelswon': 'Aerial duels won',
        'aerialduelswonpercentage': 'Aerial duels won percentage',
        'assists': 'Assists',
        'averageballpossession': 'Average ball possession',
        'avgrating': 'Avg rating',
        'ballrecovery': 'Ball recovery',
        'bigchances': 'Big chances',
        'bigchancesagainst': 'Big chances against',
        'bigchancescreated': 'Big chances created',
        'bigchancescreatedagainst': 'Big chances created against',
        'bigchancesmissed': 'Big chances missed',
        'bigchancesmissedagainst': 'Big chances missed against',
        'blockedscoringattempt': 'Blocked scoring attempt',
        'blockedscoringattemptagainst': 'Blocked scoring attempt against',
        'cleansheets': 'Clean sheets',
        'clearances': 'Clearances',
        'clearancesagainst': 'Clearances against',
        'clearancesoffline': 'Clearances off line',
        'corners': 'Corners',
        'cornersagainst': 'Corners against',
        'crossessuccessfulagainst': 'Crosses successful against',
        'crossestotalagainst': 'Crosses total against',
        'dribbleattempts': 'Dribble attempts',
        'dribbleattemptstotalagainst': 'Dribble attempts total against',
        'dribbleattemptswonagainst': 'Dribble attempts won against',
        'duelswon': 'Duels won',
        'duelswonpercentage': 'Duels won percentage',
        'errorsleadingtogoal': 'Errors leading to goal',
        'errorsleadingtogoalagainst': 'Errors leading to goal against',
        'errorsleadingtoshot': 'Errors leading to shot',
        'errorsleadingtoshotagainst': 'Errors leading to shot against',
        'fastbreakgoals': 'Fast break goals',
        'fastbreakshots': 'Fast break shots',
        'fastbreaks': 'Fast breaks',
        'fouls': 'Fouls',
        'freekickgoals': 'Free kick goals',
        'freekickshots': 'Free kick shots',
        'freekicks': 'Free kicks',
        'goalkicks': 'Goal kicks',
        'goalsconceded': 'Goals conceded',
        'goalsfrominsidethebox': 'Goals from inside the box',
        'goalsfromoutsidethebox': 'Goals from outside the box',
        'goalsscored': 'Goals scored',
        'groundduelswon': 'Ground duels won',
        'groundduelswonpercentage': 'Ground duels won percentage',
        'headedgoals': 'Headed goals',
        'hitwoodwork': 'Hit woodwork',
        'hitwoodworkagainst': 'Hit woodwork against',
        'id': 'Id',
        'interceptions': 'Interceptions',
        'interceptionsagainst': 'Interceptions against',
        'keypassesagainst': 'Key passes against',
        'lastmantackles': 'Last man tackles',
        'leftfootgoals': 'Left foot goals',
        'longballssuccessfulagainst': 'Long balls successful against',
        'longballstotalagainst': 'Long balls total against',
        'matches': 'Matches',
        'offsides': 'Offsides',
        'offsidesagainst': 'Offsides against',
        'oppositionhalfpasstotalagainst': 'Opposition half passes total against',
        'owngoals': 'Own goals',
        'ownhalfpasstotalagainst': 'Own half passes total against',
        'penaltiescommited': 'Penalties commited',
        'penaltiestaken': 'Penalties taken',
        'penaltygoals': 'Penalty goals',
        'penaltygoalsconceded': 'Penalty goals conceded',
        'possessionlost': 'Possession lost',
        'redcards': 'Red cards',
        'redcardsagainst': 'Red cards against',
        'rightfootgoals': 'Right foot goals',
        'saves': 'Saves',
        'shots': 'Shots',
        'shotsagainst': 'Shots against',
        'shotsblockedagainst': 'Shots blocked against',
        'shotsfrominsidethebox': 'Shots from inside the box',
        'shotsfrominsidetheboxagainst': 'Shots from inside the box against',
        'shotsfromoutsidethebox': 'Shots from outside the box',
        'shotsfromoutsidetheboxagainst': 'Shots from outside the box against',
        'shotsofftarget': 'Shots off target',
        'shotsofftargetagainst': 'Shots off target against',
        'shotsontarget': 'Shots on target',
        'shotsontargetagainst': 'Shots on target against',
        'successfuldribbles': 'Successful dribbles',
        'tackles': 'Tackles',
        'tacklesagainst': 'Tackles against',
        'throwins': 'Throw ins',
        'totalaerialduels': 'Total aerial duels',
        'totalcrosses': 'Total crosses',
        'totalduels': 'Total duels',
        'totalefinalthirdpassesagainst': 'Total final third passes against',
        'totalgroundduels': 'Total ground duels',
        'totallongballs': 'Total long balls',
        'totaloppositionhalfpasses': 'Total opposition half passes',
        'totalownhalfpasses': 'Total own half passes',
        'totalpasses': 'Total passes',
        'totalpassesagainst': 'Total passes against',
        'yellowcards': 'Yellow cards',
        'yellowcardsagainst': 'Yellow cards against',
        'yellowredcards': 'Yellow red cards'
    }
    
    stats_renommes = {}
    for cle, valeur in stats.items():
        if cle in mapping:
            stats_renommes[mapping[cle]] = valeur
        else:
            stats_renommes[cle] = valeur  # Garder les autres
    
    # Ajouter le nom de l'équipe
    stats_renommes['name'] = nom_club
    
    return stats_renommes

# --- COPIE DES FONCTIONS DES 6 PROGRAMMES (adaptées pour retourner les résultats) ---

def calculer_kpis_cles(stats):
    """Version adaptée du programme 1"""
    m = stats.get('Matches', 1)
    shots_on_target = stats.get('Shots on target', 0)
    
    return {
        'shooting_efficiency': stats.get('Goals scored', 0) / max(1, shots_on_target) if shots_on_target > 0 else 0,
        'defensive_solidity': (2.0 - stats.get('Goals conceded', 0) / m),
        'chance_creation': stats.get('Big chances created', 0) / m,
        'physical_dominance': stats.get('Duels won percentage', 0) / 100,
        'ball_control': stats.get('Average ball possession', 0) / 100,
        'clean_sheet_rate': stats.get('Clean sheets', 0) / m
    }

def score_puissance_cible(kpi):
    score = (
        kpi['shooting_efficiency'] * 0.25 +
        kpi['defensive_solidity'] * 0.20 +
        kpi['chance_creation'] * 0.20 +
        kpi['physical_dominance'] * 0.15 +
        kpi['ball_control'] * 0.10 +
        kpi['clean_sheet_rate'] * 0.10
    )
    return score

def predire_resultat_cible_adaptee(team1_stats, team2_stats, home_team_name=None):
    kpi1 = calculer_kpis_cles(team1_stats)
    kpi2 = calculer_kpis_cles(team2_stats)
    
    score1 = score_puissance_cible(kpi1)
    score2 = score_puissance_cible(kpi2)
    
    # Utiliser les noms passés en paramètre pour le bonus domicile
    if home_team_name == team1_stats['name']:
        score1 += 0.08
    elif home_team_name == team2_stats['name']:
        score2 += 0.08
    
    difference = score1 - score2
    seuil = 0.05
    
    if abs(difference) < seuil:
        return "Match Nul", 0
    elif difference > 0:
        return f"Victoire {team1_stats['name']}", 1
    else:
        return f"Victoire {team2_stats['name']}", 2

def calculer_lambda_ultra_precis_adapte(team, opponent):
    """Version adaptée du programme 2"""
    m = team.get('Matches', 1)
    
    base_historique = (team.get('Goals scored', 0) / m + opponent.get('Goals conceded', 0) / m) / 2
    big_chance_weight = 0.4
    shot_on_target_weight = 0.2
    xg_avance = (
        (team.get('Big chances created', 0) / m * big_chance_weight) +
        (team.get('Shots on target', 0) / m * shot_on_target_weight)
    )
    
    inside_box_ratio = team.get('Shots from inside the box', 0) / max(1, team.get('Shots', 1))
    outside_box_ratio = team.get('Shots from outside the box', 0) / max(1, team.get('Shots', 1))
    qualite_tir = (inside_box_ratio * 0.3) - (outside_box_ratio * 0.1)
    
    pressure_offensive = (
        (team.get('Accurate opposition half passes', 0) / m) * 0.0005 +
        (team.get('Corners', 0) / m) * 0.05
    )
    
    superiorite_physique = (team.get('Duels won percentage', 0) / 100) * 0.1
    
    chaos_adversaire = (
        (opponent.get('Errors leading to goal', 0) / m * 0.3) +
        (opponent.get('Errors leading to shot', 0) / m * 0.1) +
        (team.get('Hit woodwork', 0) / m * 0.2)
    )
    
    efficacite_defensive = (
        (opponent.get('Clean sheets', 0) / m * -0.2) +
        (opponent.get('Interceptions', 0) / m * -0.02)
    )
    
    lambda_total = (
        base_historique * 0.4 +
        xg_avance * 0.3 +
        qualite_tir * 0.15 +
        pressure_offensive * 0.1 +
        superiorite_physique * 0.05 +
        chaos_adversaire
    ) + efficacite_defensive
    
    return max(0.1, lambda_total)

def analyser_total_buts_adapte_sure(t1, t2):
    """Version adaptée du programme 2 - Une seule recommandation sure"""
    l1 = calculer_lambda_ultra_precis_adapte(t1, t2)
    l2 = calculer_lambda_ultra_precis_adapte(t2, t1)
    total_lambda = l1 + l2

    # Seuil pour les buts : 2.5
    # On ne recommande que si on est suffisamment loin du seuil (par exemple 0.3 de marge)
    if total_lambda > 2.8:  # Plus grand que 2.5 + 0.3
        recommendation = f"OVER 2.5 buts"
    elif total_lambda < 2.2:  # Plus petit que 2.5 - 0.3
        recommendation = f"UNDER 2.5 buts"
    else:
        # Trop proche du seuil, pas sûr
        recommendation = None

    return total_lambda, recommendation

def calculer_index_corners_ultra_adapte(team, opponent):
    """Version adaptée du programme 3"""
    m = team.get('Matches', 1)
    
    pression_offensive = (
        (team.get('Accurate opposition half passes', 0) / m * 0.015) +
        (team.get('Total crosses', 0) / m * 0.12) +
        (team.get('Total final third passes against', 0) / m * 0.008)
    )
    
    style_lateral = (
        (team.get('Accurate crosses', 0) / max(1, team.get('Total crosses', 1)) if team.get('Total crosses', 0) > 0 else 0) * 0.3 +
        (team.get('Corners', 0) / m * 0.15)
    )
    
    resistance_defensive = (
        (opponent.get('Clearances', 0) / m * 0.08) +
        (opponent.get('Shots blocked against', 0) / m * 0.1) +
        (opponent.get('Interceptions against', 0) / m * 0.05)
    )
    
    agitation_defensive = (
        (opponent.get('Fouls', 0) / m * 0.05) +
        (opponent.get('Tackles against', 0) / m * 0.03)
    )
    
    discipline_adverse = (
        (opponent.get('Yellow cards against', 0) / m * 0.02) +
        (opponent.get('Red cards against', 0) / m * 0.15)
    )
    
    agressivite_offensive = (
        (team.get('Dribble attempts', 0) / m * 0.08) +
        (team.get('Duels won percentage', 0) / 100 * 0.05) +
        (team.get('Average ball possession', 0) / 100 * 0.1)
    )
    
    reaction_defensive = (
        (team.get('Possession lost', 0) / m * 0.01)
    )
    
    index_corners = (
        pression_offensive * 0.4 +
        style_lateral * 0.25 +
        resistance_defensive * 0.2 +
        agitation_defensive * 0.1 +
        discipline_adverse * 0.05
    ) + agressivite_offensive * 0.05 + reaction_defensive * 0.01
    
    return max(0, index_corners)

def analyser_corners_adapte_sure(t1, t2):
    """Version adaptée du programme 3 - Une seule recommandation sure"""
    corners_t1 = calculer_index_corners_ultra_adapte(t1, t2)
    corners_t2 = calculer_index_corners_ultra_adapte(t2, t1)
    total_pred = corners_t1 + corners_t2

    # Seuil pour les coins : 8.5
    # On ne recommande que si on est suffisamment loin du seuil (par exemple 0.5 de marge)
    if total_pred > 9.0:  # Plus grand que 8.5 + 0.5
        recommendation = f"OVER 8.5 corners"
    elif total_pred < 8.0:  # Plus petit que 8.5 - 0.5
        recommendation = f"UNDER 8.5 corners"
    else:
        # Trop proche du seuil, pas sûr
        recommendation = None

    return total_pred, recommendation

def calculer_indice_friction_complet_adapte(team, opponent):
    """Version adaptée du programme 4"""
    m = team.get('Matches', 1)
    
    discipline_intrinseque = (
        (team.get('Yellow cards', 0) / m * 1.0) +
        (team.get('Red cards', 0) / m * 3.0) +
        (team.get('Fouls', 0) / m * 0.08)
    )
    
    agressivite_tactique = (
        (team.get('Tackles', 0) / m * 0.05) +
        (team.get('Interceptions', 0) / m * 0.03)
    )
    
    provocation = (
        (opponent.get('Dribble attempts', 0) / m * 0.08) +
        (opponent.get('Duels won percentage', 0) / 100 * 0.2)
    )
    
    pression_match = (
        abs(team.get('Average ball possession', 0) - opponent.get('Average ball possession', 0)) / 100 * 0.3
    )
    
    jeu_physique = (
        (team.get('Ground duels won', 0) / max(1, team.get('Total ground duels', 1)) * 0.15) +
        (team.get('Aerial duels won', 0) / max(1, team.get('Total aerial duels', 1)) * 0.10)
    )
    
    stress_defensif = (
        (opponent.get('Shots', 0) / m * 0.02) +
        (opponent.get('Corners', 0) / m * 0.05)
    )
    
    indice_total = (
        discipline_intrinseque * 0.4 +
        agressivite_tactique * 0.25 +
        provocation * 0.2 +
        pression_match * 0.1 +
        jeu_physique * 0.05
    ) + stress_defensif * 0.1
    
    return max(0, indice_total)

def analyser_cartons_adapte_sure(t1, t2):
    """Version adaptée du programme 4 - Une seule recommandation sure"""
    friction_t1 = calculer_indice_friction_complet_adapte(t1, t2)
    friction_t2 = calculer_indice_friction_complet_adapte(t2, t1)
    total_pred = friction_t1 + friction_t2

    # Seuil pour les cartons : 3.5
    # On ne recommande que si on est suffisamment loin du seuil (par exemple 0.3 de marge)
    if total_pred > 3.8:  # Plus grand que 3.5 + 0.3
        recommendation = f"OVER 3.5 cartons"
    elif total_pred < 3.2:  # Plus petit que 3.5 - 0.3
        recommendation = f"UNDER 3.5 cartons"
    else:
        # Trop proche du seuil, pas sûr
        recommendation = None

    return total_pred, recommendation

def calculer_kpis_cles_mi_temps_adapte(stats):
    """Version adaptée du programme 5"""
    m = stats.get('Matches', 1)
    shots_on_target = stats.get('Shots on target', 0)
    
    return {
        'early_danger': stats.get('Big chances created', 0) / m,
        'early_presence': shots_on_target / m,
        'physical_start': stats.get('Duels won percentage', 0) / 100,
        'game_control': stats.get('Average ball possession', 0) / 100,
        'early_resilience': (1 - stats.get('Errors leading to goal', 0) / m)
    }

def score_puissance_mi_temps_adapte(kpi):
    score = (
        kpi['early_danger'] * 0.30 +
        kpi['early_presence'] * 0.25 +
        kpi['physical_start'] * 0.20 +
        kpi['game_control'] * 0.15 +
        kpi['early_resilience'] * 0.10
    )
    return score

def predire_mi_temps_cible_adaptee(team1_stats, team2_stats):
    """Version adaptée du programme 5"""
    kpi1 = calculer_kpis_cles_mi_temps_adapte(team1_stats)
    kpi2 = calculer_kpis_cles_mi_temps_adapte(team2_stats)
    
    score1 = score_puissance_mi_temps_adapte(kpi1)
    score2 = score_puissance_mi_temps_adapte(kpi2)
    
    difference = score1 - score2
    seuil = 0.06
    
    if abs(difference) < seuil:
        return "Match Nul à la mi-temps"
    elif difference > 0:
        return f"{team1_stats['name']} mène à la mi-temps"
    else:
        return f"{team2_stats['name']} mène à la mi-temps"

def calculer_probabilite_btts_adapte(t1, t2):
    """Version adaptée du programme 6"""
    m1, m2 = t1.get('Matches', 1), t2.get('Matches', 1)
    
    potentiel_t1 = (t1.get('Goals scored', 0) / m1) + (t2.get('Goals conceded', 0) / m2 * 0.5)
    potentiel_t2 = (t2.get('Goals scored', 0) / m2) + (t1.get('Goals conceded', 0) / m1 * 0.5)
    
    verrou = ((t1.get('Clean sheets', 0) / m1) + (t2.get('Clean sheets', 0) / m2)) * 1.5
    
    score_btts = (potentiel_t1 + potentiel_t2) - verrou
    
    if score_btts > 2.2:
        return "BTTS OUI", True
    elif score_btts < 1.6:
        return "BTTS NON", False
    else:
        return "BTTS Indécis", None

def analyser_match_complet(id_match, nom_equipe1, nom_equipe2, home_team_name=None):
    """Analyse complète d'un match avec les 6 programmes"""
    print(f"\n{'='*60}")
    print(f"ANALYSE DU MATCH : {nom_equipe1} vs {nom_equipe2} (ID: {id_match})")
    print(f"Équipe à domicile: {home_team_name or 'Inconnue'}")
    print(f"{'='*60}")
    
    # Charger les stats
    stats1 = charger_stats_club(nom_equipe1)
    stats2 = charger_stats_club(nom_equipe2)
    
    if not stats1 or not stats2:
        print("Impossible de charger les stats. Annulation.")
        return
    
    # 1. RESULTAT FINAL
    resultat_final, code_resultat = predire_resultat_cible_adaptee(stats1, stats2, home_team_name)
    print(f"\nPRÉDICTION RÉSULTAT FINAL : {resultat_final}")
    
    # 2. TOTAL BUTS (Version Sure)
    total_buts, rec_buts = analyser_total_buts_adapte_sure(stats1, stats2)
    print(f"\nPRÉDICTION TOTAL BUTS : {total_buts:.2f}")
    if rec_buts:
        print(f"   Recommandation SÛRE buts: {rec_buts}")
    else:
        print(f"   Recommandation SÛRE buts: AUCUNE (trop proche de 2.5)")
    
    # 3. TOTAL CORNERS (Version Sure)
    total_corners, rec_corners = analyser_corners_adapte_sure(stats1, stats2)
    print(f"\n  PRÉDICTION TOTAL CORNERS : {total_corners:.2f}")
    if rec_corners:
        print(f"   Recommandation SÛRE corners: {rec_corners}")
    else:
        print(f"   Recommandation SÛRE corners: AUCUNE (trop proche de 8.5)")
    
    # 4. TOTAL CARTONS (Version Sure)
    total_cartons, rec_cartons = analyser_cartons_adapte_sure(stats1, stats2)
    print(f"\n  PRÉDICTION TOTAL CARTONS : {total_cartons:.2f}")
    if rec_cartons:
        print(f"   Recommandation SÛRE cartons: {rec_cartons}")
    else:
        print(f"   Recommandation SÛRE cartons: AUCUNE (trop proche de 3.5)")
    
    # 5. MI-TEMPS
    resultat_mt = predire_mi_temps_cible_adaptee(stats1, stats2)
    print(f"\nPRÉDICTION MI-TEMPS : {resultat_mt}")
    
    # 6. BTTS
    btts_result, btts_bool = calculer_probabilite_btts_adapte(stats1, stats2)
    print(f"\nPRÉDICTION BTTS : {btts_result}")
    
    # --- SYNTHÈSE DES MEILLEURS PARIS ---
    print(f"\n{'='*60}")
    print("SYNTHÈSE DES MEILLEURS PARIS POTENTIELS")
    print(f"{'='*60}")
    
    paris = []
    
    # Résultat
    paris.append(f"Résultat : {resultat_final}")
    
    # Total buts
    if rec_buts:
        paris.append(f"Total buts : {rec_buts}")
    else:
        paris.append(f"Total buts : ~{total_buts:.1f} buts (aucune recommandation sure)")
    
    # Total corners
    if rec_corners:
        paris.append(f"Corners : {rec_corners}")
    else:
        paris.append(f"Corners : ~{total_corners:.1f} corners (aucune recommandation sure)")
    
    # Total cartons
    if rec_cartons:
        paris.append(f"Cartons : {rec_cartons}")
    else:
        paris.append(f"Cartons : ~{total_cartons:.1f} cartons (aucune recommandation sure)")
    
    # Mi-temps
    paris.append(f"Mi-temps : {resultat_mt}")
    
    # BTTS
    paris.append(f"BTTS : {btts_result}")
    
    for pari in paris:
        print(f"  • {pari}")

def trouver_premier_match_non_joue(num_journee):
    """Trouve le premier match non joué dans la journée spécifiée"""
    root = "Premier_League_2526"
    base_dir = os.path.join(root, "Matchs_A_Venir")
    nom_fichier = f"Journee_{num_journee}.txt"
    filepath = os.path.join(base_dir, nom_fichier)
    
    if not os.path.exists(filepath):
        print(f"Fichier {nom_fichier} non trouvé dans {base_dir}")
        return None
    
    with open(filepath, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    
    match_list = []
    for ligne in lignes:
        if "#" in ligne:
            parts = ligne.strip().split("#")
            match_id = parts[0].strip()
            match_desc = parts[1].strip()
            
            # Extraire noms équipes (format: "Equipe1 vs Equipe2")
            # La première équipe est considérée comme l'équipe à domicile
            if " vs " in match_desc:
                equipe1, equipe2 = match_desc.split(" vs ", 1)
                equipe1 = equipe1.strip()
                equipe2 = equipe2.strip()
                match_list.append((match_id, equipe1, equipe2))
    
    return match_list

def main():
    print("🔍 Analyseur de Journée - Chargement des prédictions")
    num_journee = input("Quelle journée souhaitez-vous analyser ? (ex: 24) : ").strip()
    
    match_list = trouver_premier_match_non_joue(num_journee)
    
    if not match_list:
        print(f"Aucun match trouvé dans la journée {num_journee}")
        return

    print(f"\n--- {len(match_list)} match(s) trouvés dans la journée {num_journee} ---")

    for i, (id_match, equipe1, equipe2) in enumerate(match_list):
        print(f"\n--- Match {i+1}/{len(match_list)} : {equipe1} vs {equipe2} (ID: {id_match}) ---")
        
        # Demander confirmation avant d'analyser
        continuer = input("Voulez-vous analyser ce match ? (o/n) : ").lower().strip()
        if continuer in ['o', 'oui', 'y', 'yes']:
            # equipe1 est l'équipe à domicile, equipe2 est l'équipe extérieure
            analyser_match_complet(id_match, equipe1, equipe2, home_team_name=equipe1)
            print("\n" + "="*80)
            print("Fin de l'analyse de ce match.")
            print("="*80)
        else:
            print("Passage au match suivant ou arrêt.")
            continue # Passe au match suivant dans la boucle for

if __name__ == "__main__":
    main()