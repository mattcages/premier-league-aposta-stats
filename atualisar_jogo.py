import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# Import des fonctions des autres fichiers
from match_scan import scan_match_individuel, options
import club_stats # On va adapter ce fichier juste après
import player_stats # On va adapter ce fichier juste après

def actualiser_systeme():
    root_folder = "Premier_League_2526"
    base_dir = os.path.join(root_folder, "Matchs_A_Venir")
    
    if not os.path.exists(base_dir):
        print(f"Erreur : Le dossier '{base_dir}' n'existe pas.")
        return

    num_rodada = input("Quelle Rodada souhaites-tu actualiser ? (ex: 24) : ").strip()
    cible_fichier = f"Journee_{num_rodada}.txt"
    filepath = os.path.join(base_dir, cible_fichier)

    if not os.path.exists(filepath):
        print(f"Aucun fichier '{cible_fichier}' trouvé.")
        return

    print(f"\nDémarrage de l'actualisation pour la Rodada {num_rodada}...")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lignes = f.readlines()

        nouvelles_lignes = []
        for ligne in lignes:
            if "#" in ligne:
                parts = ligne.split("#")
                match_id = parts[0].strip()
                match_nom = parts[1].strip()
                
                print(f"\nVérification Match : {match_nom} (ID: {match_id})")
                
                # 1. On tente de scanner le match via match_scan
                # La fonction renvoie (home_id, away_id) si fini, sinon None
                resultat_ids = scan_match_individuel(match_id, driver)
                
                if resultat_ids:
                    home_id, away_id = resultat_ids
                    print(f"Match terminé ! Lancement de la mise à jour globale...")
                    
                    # 2. Mise à jour des Stats des 2 Clubs
                    print(f"   -> Mise à jour des stats clubs...")
                    club_stats.update_club_stats(home_id, driver)
                    club_stats.update_club_stats(away_id, driver)
                    
                    # 3. Mise à jour des Stats des Joueurs des 2 Clubs
                    print(f"   -> Mise à jour des stats joueurs (cela peut prendre du temps)...")
                    player_stats.update_all_players(home_id, driver)
                    player_stats.update_all_players(away_id, driver)
                    
                    print(f"Tout est à jour pour {match_nom}. Supprimé de la liste à venir.")
                else:
                    # Match non fini, on le garde dans le fichier
                    print(f"Match non terminé ou stats non prêtes. Conservé.")
                    nouvelles_lignes.append(ligne)
            else:
                nouvelles_lignes.append(ligne)

        # Réécriture du fichier avec seulement les matchs restants
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(nouvelles_lignes)

    except Exception as e:
        print(f"Erreur critique : {e}")
    finally:
        driver.quit()
        print("\n--- Opération d'actualisation terminée ! ---")

if __name__ == "__main__":
    actualiser_systeme()