"""Main scraper script - orchestrates the web scraping process."""
from scraper_lib import setup_logging, scrape, save_results


def main():
    setup_logging()
    print("🔍 Démarrage du scraper...")
    all_jobs = scrape()
    save_results(all_jobs)
    print(f"✅ {len(all_jobs)} offres collectées")


if __name__ == "__main__":
    main()