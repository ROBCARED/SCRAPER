# 🔍 Job Scraper & Analyzer

Outil Python qui **collecte automatiquement des offres d'emploi Data Analyst** sur Free-Work, puis les **analyse** pour faire ressortir les offres les plus intéressantes selon les compétences demandées et le salaire.

## Fonctionnement

```
Scraping (5 pages)  →  offres_emploi.csv  →  KPI 1 : score technique + salaire  →  KPI 2 : tâches / salaire  →  Top 10
```

1. **Collecte** : scraping des pages de résultats avec Requests et BeautifulSoup, export en CSV.
2. **KPI 1** (`kpi.py`) : score technique (nombre de compétences clés citées : Python, SQL, Power BI, Azure, Databricks…) et harmonisation des salaires et TJM en salaire annuel estimé.
3. **KPI 2** (`kpi2.py`) : extraction des tâches de chaque offre et calcul d'un ratio tâches / salaire pour repérer les offres les mieux rémunérées au regard de la charge demandée.
4. **Exploration** : interface Streamlit pour parcourir le top 10.

## Stack

Python · Requests · BeautifulSoup · Pandas · Streamlit

## Lancer le projet

```bash
pip install -r requirements.txt

python main.py              # scraping puis KPI 1
python main.py --kpi kpi2   # scraping puis KPI 2
streamlit run app.py        # exploration des résultats
```

Les paramètres (URL, nombre de pages, mots-clés, villes) sont dans `config.py`.
