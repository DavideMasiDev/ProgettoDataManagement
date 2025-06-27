# 🕹️ IsThereAnyDeal Price History Scraper

This scraper leverages the official **IsThereAnyDeal API** to build a complete **price history dataset** for games.

📘 **API Reference**: [IsThereAnyDeal API Docs](https://docs.isthereanydeal.com/#tag/History/operation/games-history-v2)

## 🔍 Description

This tool queries the `games/history/v2` endpoint of the IsThereAnyDeal API to collect and store historical price data of video games.  
Useful for:

- Tracking price trends over time
- Building datasets for analysis or machine learning
- Monitoring sales and deals automatically

## 📦 Output

The scraper generates a structured dataset (a CSV file) containing:

- Game Title
- Timestamps
- Historical price points and relative deals
- Regular price
- Currency

## 🛠️ Requirements

- Python 3.x
- An IsThereAnyDeal API key (free registration)

## 🚀 Quick Start

> [!WARNING]
> Before running the script, open the main Python file (scraping.py) and insert your IsThereAnyDeal API
> ```
> 
> API_KEY = "insert_your_key"
> 
> ```

- Clone the repository
```

git clone https://github.com/tuo-utente/isthereanydeal-scraper.git
cd isthereanydeal-scraper

```

- Install dependencies
```

pip install -r requirements.txt

```

- Edit games.txt to add or remove game titles

- Run the scraper
```

python scrape.py

```
