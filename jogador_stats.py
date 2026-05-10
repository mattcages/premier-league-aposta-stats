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
    """Nettoie les noms pour les dossiers et fichiers"""
    return re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")

def enregistrer_id_dans_joueurs(chemin_joueurs, p_id, p_name):
    """Enregistre l'ID et le nom dans liste_joueurs.txt"""
    fichier_chemin = os.path.join(chemin_joueurs, "liste_joueurs.txt")
    ligne = f"{p_id} # {p_name}\n"
    
    if os.path.exists(fichier_chemin):
        with open(fichier_chemin, "r", encoding="utf-8") as f:
            if str(p_id) in f.read():
                return

    with open(fichier_chemin, "a", encoding="utf-8") as f:
        f.write(ligne)

def trier_liste_joueurs(chemin_joueurs):
    """Trie le fichier liste_joueurs.txt par nom"""
    fichier_chemin = os.path.join(chemin_joueurs, "liste_joueurs.txt")
    if os.path.exists(fichier_chemin):
        with open(fichier_chemin, "r", encoding="utf-8") as f:
            lignes = f.readlines()
        
        lignes.sort(key=lambda x: x.split("#")[1].strip() if "#" in x else x)
        
        with open(fichier_chemin, "w", encoding="utf-8") as f:
            f.writelines(lignes)

def formater_toutes_stats(stats_json):
    """Extrait proprement toutes les statistiques du JSON"""
    s = stats_json.get('statistics', {})
    if not s:
        return "Aucune statistique disponible."
    
    rapport = []
    for cle, valeur in s.items():
        nom_propre = re.sub(r'([a-z])([A-Z])', r'\1 \2', cle).capitalize()
        rapport.append(f"{nom_propre:<35} | {valeur}")
    
    return "\n".join(rapport)

def update_all_players(club_id, driver):
    """Fonction utilisée pour mettre à jour tout l'effectif d'un club"""
    dossier_parent = "Premier_League_2526"
    
    # 1. Nom du club
    driver.get(f"https://www.sofascore.com/api/v1/team/{club_id}")
    time.sleep(1.5)
    try:
        data_club = json.loads(driver.find_element("tag name", "body").text)
        club_nom = data_club['team']['name']
    except:
        print(f"Club {club_id} introuvable."); return

    # 2. Liste des joueurs
    driver.get(f"https://www.sofascore.com/api/v1/team/{club_id}/players")
    time.sleep(1.5)
    try:
        data_equipe = json.loads(driver.find_element("tag name", "body").text)
        joueurs = data_equipe.get('players', [])
    except:
        print(f"Erreur liste joueurs pour {club_nom}"); return

    # --- NOUVEAU CHEMIN : Premier_League_2526 / Clubs / [Nom_Club] / Stats_Joueurs ---
    chemin_club = os.path.join(dossier_parent, "Clubs", clean_name(club_nom))
    chemin_joueurs = os.path.join(chemin_club, "Stats_Joueurs")
    if not os.path.exists(chemin_joueurs): os.makedirs(chemin_joueurs, exist_ok=True)

    total = len(joueurs)
    print(f"\nEffectif : {club_nom.upper()} ({total} joueurs)")
    
    for i, item in enumerate(joueurs):
        p = item['player']
        p_name, p_id = p['name'], p['id']

        print(f" > {i+1}/{total} : {p_name}", end="\r")

        # Sauvegarde de l'ID
        enregistrer_id_dans_joueurs(chemin_joueurs, p_id, p_name)

        if i > 0 and i % 10 == 0: time.sleep(4)

        # 3. Stats Saison (PL=17, Saison=76986)
        url_stats = f"https://www.sofascore.com/api/v1/player/{p_id}/unique-tournament/17/season/76986/statistics/overall"
        driver.get(url_stats)
        time.sleep(random.uniform(0.8, 1.2))
        
        try:
            res_stats = driver.find_element("tag name", "body").text
            data_stats = json.loads(res_stats)
            if 'statistics' in data_stats:
                with open(os.path.join(chemin_joueurs, f"{clean_name(p_name)}.txt"), "w", encoding="utf-8") as f:
                    f.write(f"{'='*50}\nJOUEUR : {p_name.upper()}\nID     : {p_id}\nCLUB   : {club_nom.upper()}\n{'='*50}\n\n")
                    f.write(formater_toutes_stats(data_stats))
        except:
            continue

    trier_liste_joueurs(chemin_joueurs)
    print(f"\nTerminé pour {club_nom}.")

def main():
    print("Initialisation du Scanner de Joueurs...")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    try:
        while True:
            club_id = input("\nEntrez l'ID du Club SofaScore (ou 'fin') : ")
            if club_id.lower() == 'fin': break
            if club_id.isdigit():
                update_all_players(club_id, driver)
            else:
                print("Erreur : ID non valide.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()