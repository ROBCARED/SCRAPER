import re
from typing import List, Tuple, Optional
import pandas as pd


def calculer_score_tech(texte: str, keywords: list) -> int:
    """Calculate technical skills score from text."""
    if not isinstance(texte, str):
        return 0
    texte = texte.lower()
    score = 0
    for mot in keywords:
        if mot in texte:
            score += 1
    return score


def harmoniser_salaire(valeur, txt: str = None) -> float:
    """Normalize salary to annual estimate."""
    if txt is None:
        txt = str(valeur).lower()
    else:
        txt = txt.lower()
    
    # Extract all numbers
    nombres = re.findall(r'\d+', txt)
    if not nombres:
        return 0
    
    # Average if range (ex: 45-55 -> 50)
    nums = [int(n) for n in nombres]
    montant = sum(nums) / len(nums)
    
    # Conversion logic
    # If TJM (Freelance) -> multiply by 220 days
    if '/j' in txt or 'tjm' in txt or (montant > 200 and montant < 1500):
        return montant * 220
    
    # If in K€ (ex: 45k) -> multiply by 1000
    if 'k' in txt:
        return montant * 1000
    
    # If small number (ex: 45) -> probably K€
    if montant < 200:
        return montant * 1000
        
    return montant


def analyze_jobs(df: pd.DataFrame, keywords: list) -> pd.DataFrame:
    """Add KPI columns to job dataframe."""
    df = df.copy()
    
    # Fill missing values
    df['Description'] = df['Description'].fillna("")
    df['Salaire/TJM'] = df['Salaire/TJM'].fillna("N/C")
    
    # Calculate scores
    df['tech_score'] = df['Description'].apply(lambda x: calculer_score_tech(x, keywords))
    df['salaire_annuel_estime'] = df['Salaire/TJM'].apply(harmoniser_salaire)
    
    # Sort by criteria
    df = df.sort_values(by=['tech_score', 'salaire_annuel_estime'], ascending=[False, False])
    
    return df


def extract_tasks(desc: str, keywords: list) -> Tuple[List[str], int]:
    """Return list of matched keywords and the complexity index (count).

    desc: job description
    keywords: list of technology keywords
    """
    if not isinstance(desc, str) or not desc:
        return [], 0
    txt = desc.lower()
    found = [k for k in keywords if k in txt]
    return found, len(found)


def calc_ratio_taches_par_salaire(complexite, salaire_annuel) -> float:
    """Compute ratio = complexite / salaire_annuel (returns None if invalid)."""
    try:
        s = float(salaire_annuel)
    except Exception:
        return None
    if s <= 0:
        return None
    try:
        return round(float(complexite) / s, 8)
    except Exception:
        return None


def analyze_tasks(df: pd.DataFrame, keywords: list) -> pd.DataFrame:
    """Add task list, complexity and ratio KPI to the dataframe.

    Adds columns: `liste_taches`, `complexite`, `salaire_estime`, `ratio_taches_par_salaire`.
    """
    df = df.copy()
    # Ensure columns exist before calling .fillna() to avoid analyzer/linter warnings
    if 'Description' not in df.columns:
        df['Description'] = ""
    else:
        df['Description'] = df['Description'].fillna("")

    if 'Salaire/TJM' not in df.columns:
        df['Salaire/TJM'] = "N/C"
    else:
        df['Salaire/TJM'] = df['Salaire/TJM'].fillna("N/C")

    # Ensure salary estimate exists
    df['salaire_estime'] = df['Salaire/TJM'].apply(harmoniser_salaire)

    # Tasks extraction and complexity
    df['liste_taches'] = df['Description'].apply(lambda d: extract_tasks(d, keywords)[0])
    df['complexite'] = df['Description'].apply(lambda d: extract_tasks(d, keywords)[1])

    # KPI ratio (complexity / annual salary)
    df['ratio_taches_par_salaire'] = df.apply(
        lambda r: calc_ratio_taches_par_salaire(r['complexite'], r['salaire_estime']), axis=1
    )

    return df
