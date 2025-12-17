import re
from typing import Dict


def extract_job(job_tag) -> Dict[str, str]:
    """Extract job information from a job card element."""
    from config import FRENCH_CITIES
    
    title_tag = job_tag.find("h1") or job_tag.find("h2") or job_tag.find("h3")
    if not title_tag:
        return {}
    
    title = title_tag.get_text(strip=True).replace("Offre d'emploi", "").strip()
    
    company_tag = job_tag.find('div', class_='font-bold')
    company = company_tag.get_text(strip=True) if company_tag else ""

    description = "Voir détails"
    texts = list(job_tag.stripped_strings)
    if texts:
        longest = max(texts, key=len)
        if len(longest) > 60:
            description = longest.replace("\n", " ").strip()

    location = "France / Remote"
    salary = "N/C"
    
    for t in texts:
        if len(t) > 50:
            continue
        if t == title or t == company:
            continue
        if ("€" in t or "TJM" in t) and len(t) < 30:
            salary = t
            continue
        if re.search(r"\(\d{2,3}\)", t) or re.search(r"\b\d{5}\b", t):
            if "€" not in t:
                location = t
                continue
        if location == "France / Remote":
            if any(c in t for c in FRENCH_CITIES) and len(t) < 30 and "€" not in t:
                location = t

    a_tag = job_tag.find("a", href=True)
    link = f"https://www.free-work.com{a_tag['href']}" if a_tag else "Non trouvé"

    location = location.replace("Lieu :", "").strip()

    return {
        "Poste": title,
        "Entreprise": company,
        "Ville": location,
        "Salaire/TJM": salary,
        "Description": description,
        "Lien": link,
    }
