import json
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

USERNAME = "KpyBara"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT_FILE = "data/contributions.json"


def fetch_contributions():

    print("[+] ACCESSING GITHUB CONTRIBUTION NETWORK...")
    print(f"[+] TARGET: {USERNAME}")

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(URL, headers=headers, timeout=30)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    contributions = []

    cells = soup.select("td.ContributionCalendar-day")

    if not cells:
        raise RuntimeError("Nenhuma célula de contribuição encontrada.")

    for cell in cells:

        date = cell.get("data-date")
        level_text = cell.get("data-level") or "0"

        if date is None:
            continue

        try:
            level = int(level_text)
        except (TypeError, ValueError):
            continue

        contributions.append({"date": date, "level": level})

    print(f"[+] {len(contributions)} contribution cells received.")

    return contributions


def calculate_statistics(contributions):

    total_level = sum(item["level"] for item in contributions)

    active_days = sum(1 for item in contributions if item["level"] > 0)

    best_level = max((item["level"] for item in contributions), default=0)

    return {
        "total_level": total_level,
        "active_days": active_days,
        "best_level": best_level,
    }


def main():

    contributions = fetch_contributions()

    statistics = calculate_statistics(contributions)

    data = {
        "username": USERNAME,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "statistics": statistics,
        "contributions": contributions,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        json.dump(data, file, indent=2, ensure_ascii=False)

    print("[+] DATA SAVED.")
    print(f"[+] OUTPUT: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
