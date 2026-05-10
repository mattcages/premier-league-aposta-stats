import os
import json
import time
import re
import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

options = Options()
options.add_argument("-headless") 
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0")
options.set_preference("devtools.jsonview.enabled", False)

def clean_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")

def update_club_stats(current_id, driver):
    """Fonction isolée pour mettre à jour un club spécifique"""
    root = "Premier_League_2526"
    
    try:
        # 1. Récupération du nom de l'équipe
        driver.get(f"https://www.sofascore.com/api/v1/team/{current_id}")
        time.sleep(random.uniform(1.5, 2.0))
        res_info = driver.find_element("tag name", "body").text
        if not res_info.strip().startswith('{'): return
        
        data_info = json.loads(res_info)
        team_name = data_info['team']['name']

        # 2. Requête des statistiques saisonnières
        url_stats = f"https://www.sofascore.com/api/v1/team/{current_id}/unique-tournament/17/season/76986/statistics/overall"
        driver.get(url_stats)
        time.sleep(random.uniform(2.0, 3.0))
        
        res_stats = driver.find_element("tag name", "body").text
        if not res_stats.strip().startswith('{'): return
        data_stats = json.loads(res_stats)

        if 'statistics' in data_stats:
            # --- NOUVELLE STRUCTURE : Premier_League_2526 / Clubs / Nom_Club ---
            dossier_club = os.path.join(root, "Clubs", clean_name(team_name))
            if not os.path.exists(dossier_club): 
                os.makedirs(dossier_club, exist_ok=True)

            chemin_stats = os.path.join(dossier_club, "stats_club.txt")

            with open(chemin_stats, "w", encoding="utf-8") as f:
                f.write(f"STATISTIQUES SAISON : {team_name.upper()}\n")
                f.write(f"ID SOFASCORE : {current_id}\n")
                f.write(f"COMPÉTITION  : Premier League 25/26\n")
                f.write("="*60 + "\n\n")
                
                stats = data_stats['statistics']
                for key in sorted(stats.keys()):
                    label = re.sub(r'([a-z])([A-Z])', r'\1 \2', key).capitalize()
                    f.write(f"{label:<35} : {stats[key]}\n")

            # --- ARCHIVAGE DE L'ID (Optionnel, dans la racine) ---
            chemin_liste_ids = os.path.join(root, "ids_clubs_premier_league.txt")
            deja_present = False
            if os.path.exists(chemin_liste_ids):
                with open(chemin_liste_ids, "r", encoding="utf-8") as f_ids:
                    if str(current_id) in f_ids.read(): deja_present = True
            
            if not deja_present:
                with open(chemin_liste_ids, "a", encoding="utf-8") as f_ids:
                    f_ids.write(f"{current_id} # {team_name}\n")

            print(f"Mis à jour : {team_name} (ID: {current_id})")
    except Exception as e:
        print(f"Erreur sur l'ID {current_id}")

def main():
    print("Initialisation du Scanner de Clubs...")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    try:
        # Déblocage initial
        driver.get("https://www.sofascore.com")
        time.sleep(4)

        while True:
            print("\n" + "="*50)
            start_id_input = input("👉 ID Équipe de départ (ou 'fin') : ")
            if start_id_input.lower() == 'fin': break
            nb_input = input("🔢 Combien d'IDs à scanner : ")
            
            if not start_id_input.isdigit() or not nb_input.isdigit():
                print("Erreur : Entre des nombres."); continue

            id_actuel = int(start_id_input)
            nb_a_scanner = int(nb_input)

            for i in range(nb_a_scanner):
                current_id = id_actuel + i
                if i > 0 and i % 10 == 0:
                    time.sleep(10)

                print(f"Analyse ID: {current_id} ({i+1}/{nb_a_scanner})", end="\r")
                update_club_stats(current_id, driver)

    finally:
        driver.quit()
        print("Système déconnecté.")

if __name__ == "__main__":
    main()