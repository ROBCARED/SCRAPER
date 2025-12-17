import logging
import time
import random
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
import pandas as pd

from config import BASE_URL, HEADERS, PAGES_TO_SCRAPE, OUTPUT_CSV
from parser import extract_job


def setup_logging():
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def fetch_page(session: requests.Session, page: int) -> BeautifulSoup:
    """Fetch a single page from the website."""
    url = f"{BASE_URL}{page}"
    resp = session.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def scrape(pages: int = PAGES_TO_SCRAPE) -> List[Dict[str, str]]:
    """Scrape job listings."""
    session = requests.Session()
    results: List[Dict[str, str]] = []

    for page in range(1, pages + 1):
        logging.info(f"Page {page}...")
        try:
            soup = fetch_page(session, page)
        except Exception as e:
            logging.error(f"Erreur récupération page {page}: {e}")
            break

        job_cards = soup.find_all("div", class_="cursor-pointer")
        if not job_cards:
            logging.info("Fin des résultats ou structure modifiée.")
            break

        for card in job_cards:
            try:
                data = extract_job(card)
                if data:
                    results.append(data)
                    logging.info(
                        f"Collecté: {data.get('Entreprise', '')[:20]} | {data.get('Poste', '')[:20]}"
                    )
            except Exception:
                continue

        time.sleep(random.uniform(1, 3))

    return results


def save_results(jobs: List[Dict[str, str]]):
    """Save scraped jobs to CSV."""
    logging.info(f"Conversion en DataFrame ({len(jobs)} offres)")
    df = pd.DataFrame(jobs)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig", sep=";")
    logging.info(f"Terminé — fichier écrit: {OUTPUT_CSV}")
