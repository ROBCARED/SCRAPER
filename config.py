# Configuration centralisée
BASE_URL = "https://www.free-work.com/fr/tech-it/jobs?query=Data+Analyst&page="

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )
}

OUTPUT_CSV = "offres_emploi.csv"
RESULTS_CSV = "resultats_analyses_kpi.csv"
PAGES_TO_SCRAPE = 5

# KPI Configuration
KPI_KEYWORDS = [
    'python', 'sql', 'power bi', 'powerbi', 'tableau', 'excel', 'vba',
    'sas', 'r', 'azure', 'aws', 'gcp', 'snowflake', 'databricks', 
    'etl', 'talend', 'git', 'jira', 'agile', 'scrum', 'dax', 'modeling'
]

FRENCH_CITIES = [
    "Paris", "Lyon", "Bordeaux", "Nantes", "Lille",
    "Toulouse", "Nice", "Marseille", "Rennes", "Strasbourg",
    "Ile-de-France",
]
