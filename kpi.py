"""KPI analysis script - analyzes job offers based on technical requirements and salary."""
import pandas as pd

from config import OUTPUT_CSV, RESULTS_CSV, KPI_KEYWORDS
from analyzer import analyze_jobs


def main():
    print("📊 Chargement des données...")
    try:
        df = pd.read_csv(OUTPUT_CSV, sep=';')
    except FileNotFoundError:
        print(f"❌ Fichier '{OUTPUT_CSV}' introuvable.")
        return

    # Analyze jobs
    df_final = analyze_jobs(df, KPI_KEYWORDS)

    # Display top 10
    print("\n🏆 TOP 10 DES OFFRES LES PLUS CONCRÈTES :\n")
    cols = ['Poste', 'Entreprise', 'Salaire/TJM', 'salaire_annuel_estime', 'tech_score']
    print(df_final[cols].head(10).to_string(index=False))

    # Save results
    df_final.to_csv(RESULTS_CSV, index=False, sep=';', encoding='utf-8-sig')
    print(f"\n✅ Fichier analysé généré : '{RESULTS_CSV}'")


if __name__ == "__main__":
    main()