import pandas as pd
from analyzer import analyze_tasks
from config import KPI_KEYWORDS


def main():
    try:
        df = pd.read_csv("resultats_analyses_kpi.csv", sep=';')
    except FileNotFoundError:
        print("❌ Fichier 'resultats_analyses_kpi.csv' introuvable. Lancez le script kpi.py d'abord.")
        return

    df_analyzed = analyze_tasks(df, KPI_KEYWORDS)
    df_clean = df_analyzed[df_analyzed['salaire_estime'] > 0].copy()

    print("\n📌 Données filtrées pour le KPI — calcul et sélection du Top 10\n")

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1200)

    # Tri et sélection du Top 10 global
    df_sorted = df_clean.sort_values(by='ratio_taches_par_salaire', ascending=True)
    cols_display = ['Poste', 'Entreprise', 'liste_taches', 'complexite', 'salaire_estime', 'ratio_taches_par_salaire', 'Lien']
    top10 = df_sorted.head(10)[cols_display].copy()
    top10.rename(columns={
        'liste_taches': 'Liste_taches',
        'complexite': 'Complexite',
        'salaire_estime': 'Salaire_annuel_estime',
        'ratio_taches_par_salaire': 'Ratio_Taches_par_Salaire'
    }, inplace=True)

    # Affichage propre (format des floats)
    print("\n🏆 TOP 10 GLOBAL (INDICE_TÂCHES / SALAIRE) :\n")
    print(top10.to_string(index=False, float_format="{:.8g}".format))

    # Sauvegarde uniquement du Top 10
    top10.to_csv('kpi_tasks_ratio_top10.csv', index=False, sep=';', encoding='utf-8-sig')
    print("\n✅ Top 10 sauvegardé dans 'kpi_tasks_ratio_top10.csv'")


if __name__ == "__main__":
    main()
