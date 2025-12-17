"""Main entry point - orchestrates scraping and chosen KPI analysis.

Usage examples:
  python main.py                # runs scraper then default KPI (kpi)
  python main.py --kpi kpi2     # runs scraper then kpi2 analysis
"""
import sys
import argparse

from scraper import main as run_scraper
import kpi
import kpi2


def main():
    parser = argparse.ArgumentParser(description="Run scraper and analysis")
    parser.add_argument("--kpi", choices=["kpi", "kpi2"], default="kpi",
                        help="Which KPI analysis to run after scraping")
    args = parser.parse_args()

    print("=" * 50)
    print("🚀 JOB SCRAPER & ANALYZER")
    print("=" * 50)

    # Step 1: Scrape jobs
    print("\n[1/2] SCRAPING...")
    try:
        run_scraper()
    except Exception as e:
        print(f"❌ Erreur scraping: {e}")
        sys.exit(1)

    # Step 2: Analyze jobs with chosen KPI
    print("\n[2/2] ANALYSIS...")
    try:
        if args.kpi == "kpi":
            kpi.main()
        else:
            kpi2.main()
    except Exception as e:
        print(f"❌ Erreur analysis: {e}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("✅ PROCESS COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    main()
