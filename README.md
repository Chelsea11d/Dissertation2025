# Vegan Nutrition Tracker 🍎

A multi-page Streamlit application for personalised vegan nutrition tracking, product recommendations, and analytics — built as part of an MSc Data Science and AI dissertation.

**🔗 Live demo:** _[add your Streamlit Cloud link here once deployed]_

## Features

- **Nutrition Tracker** — select nutrients and products, get real-time intake totals scaled by portion size, and see personalised gram-level recommendations to close nutrient gaps
- **Add Item** — user-submitted product suggestions with full nutrient profiles, saved with timestamps
- **Feedback** — lightweight feedback collection with CSV export
- **Analytics** — bar charts comparing consumed vs. target nutrients, deficit alerts, and popular product tracking

## Tech Stack

- **Python** with **pandas** for data processing
- **Streamlit** for the multi-page web interface
- Custom recommendation logic using nutrient-density ranking

## Dataset

`vegan_products_expanded.csv` — a curated dataset of 25 vegan products across 8 food categories, with per-100g nutritional values (protein, carbs, sugar, fats, vitamins, minerals, calories).

## Run locally

```bash
pip install -r requirements.txt
streamlit run 1_Nutrition_Tracker.py
```

## About

Built by Chelsea Dass as part of an MSc dissertation in Data Science and Artificial Intelligence, Oxford Brookes University (2025).
