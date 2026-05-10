import os
import json
import time
import re
import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# --- CONFIGURATION ---
options = Options()
options.add_argument("-headless") 
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0")
options.set_preference("devtools.jsonview.enabled", False)

def clean_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")

def generer_rapport_stats(home_team, away_team, score, tournament, round_num, match_id, stats_data):
    """Génère la fiche détaillée pour le fichier .txt"""
    rapport = [
        "="*65,
        f"COMPETITION : {tournament.upper()}",
        f"RODADA       : {round_num}",
        f"MATCH ID     : {match_id}",
        f"SCORE        : {home_team.upper()} {score} {away_team.upper()}",
        "="*65 + "\n"
    ]
    if 'statistics' in stats_data and len(stats_data['statistics']) > 0:
        groups = stats_data['statistics'][0]['groups']
        rapport.append(f"{'STATISTIQUE':<30} | {home_team[:12]:<12} | {away_team[:12]}")
        rapport.append("-" * 65)
        for group in groups:
            rapport.append(f"\n--- {group['groupName'].upper()} ---")
            for item in group['statisticsItems']:
                rapport.append(f"{item['name']:<30} | {item['home']:<12} | {item['away']}")
    return "\n".join(rapport)

def scan_match_individuel(current_id, driver):
    """Fonction utilisée par l'actualiseur automatique"""
    root = "Premier_League_2526"
    try:
        driver.get(f"https://www.sofascore.com/api/v1/event/{current_id}")
        time.sleep(random.uniform(1.5, 2.5))
        res_info = driver.find_element("tag name", "body").text
        if not res_info.strip().startswith('{'): return None
        data_info = json.loads(res_info)
        if 'event' not in data_info: return None
        
        ev = data_info['event']
        rodada = ev.get('roundInfo', {}).get('round', '?')
        home = ev['homeTeam']['name']
        away = ev['awayTeam']['name']
        home_id = ev['homeTeam']['id']
        away_id = ev['awayTeam']['id']
        status = ev['status']['type']

        if status == 'finished':
            driver.get(f"https://www.sofascore.com/api/v1/event/{current_id}/statistics")
            time.sleep(random.uniform(1.5, 2.5))
            data_stats = json.loads(driver.find_element("tag name", "body").text)

            if 'statistics' in data_stats:
                score_text = f"{ev['homeScore'].get('display', 0)}-{ev['awayScore'].get('display', 0)}"
                fiche_txt = generer_rapport_stats(home, away, score_text, ev['tournament']['name'], rodada, current_id, data_stats)
                
                for equipe in [home, away]:
                    adversaire = away if equipe == home else home
                    # NOUVELLE STRUCTURE : Clubs / Nom / Matchs
                    chemin = os.path.join(root, "Clubs", clean_name(equipe), "Matchs")
                    if not os.path.exists(chemin): os.makedirs(chemin, exist_ok=True)
                    
                    nom_fichier = f"Rodada_{rodada}_vs_{clean_name(adversaire)}.txt"
                    with open(os.path.join(chemin, nom_fichier), "w", encoding="utf-8") as f:
                        f.write(fiche_txt)
                
                print(f"Match fini enregistré : {home} vs {away} (ID: {current_id})")
                return (home_id, away_id)
        else:
            # MATCH A VENIR
            dossier_avenir = os.path.join(root, "Matchs_A_Venir")
            if not os.path.exists(dossier_avenir): os.makedirs(dossier_avenir, exist_ok=True)
            
            fichier_rodada = os.path.join(dossier_avenir, f"Rodada_{rodada}.txt")
            existe = False
            if os.path.exists(fichier_rodada):
                with open(fichier_rodada, "r", encoding="utf-8") as f:
                    if str(current_id) in f.read(): existe = True
            
            if not existe:
                with open(fichier_rodada, "a", encoding="utf-8") as f:
                    f.write(f"{current_id} # {home} vs {away}\n")
                print(f"Match à venir noté (ID: {current_id}) : {home} vs {away}")
        return None
    except:
        return None

def main():
    print("Initialisation du système...")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    try:
        while True:
            start_id_input = input("ID de départ (ou 'fin') : ")
            if start_id_input.lower() == 'fin': break
            nb_input = input("Nombre d'IDs à scanner : ")
            
            if not start_id_input.isdigit() or not nb_input.isdigit():
                print("Erreur : Entre des nombres."); continue

            id_actuel = int(start_id_input)
            nb_a_scanner = int(nb_input)

            for i in range(nb_a_scanner):
                current_id = id_actuel + i
                if i > 0 and i % 10 == 0:
                    print(f"Pause de sécurité (10s)...")
                    time.sleep(10)

                print(f"Analyse ID: {current_id} ({i+1}/{nb_a_scanner})", end="\r")
                scan_match_individuel(current_id, driver)
            print(f"\nScan terminé.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()