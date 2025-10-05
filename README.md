# Finance Importer

A lightweight CLI tool to import personal finance holdings into MySQL.
This project is designed to take screenshots of your investments, convert them into a JSON file via ChatGPT, and then import them into normalized tables (`holdings` + `holding_meta`) in MySQL.

---

## 📦 Setup

```bash
git clone https://github.com/pokhiii/finance.git
cd finance-importer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure your DB credentials:

```dotenv
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=finance
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE `holdings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `asset_name` VARCHAR(255) NOT NULL,
  `asset_type` VARCHAR(50) DEFAULT NULL,
  `institution` VARCHAR(255) DEFAULT NULL,
  `current_value` DECIMAL(15,2) NOT NULL,
  `currency` VARCHAR(10) DEFAULT 'INR',
  `updated_at` DATE NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `holding_meta` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `holding_id` INT NOT NULL,
  `meta_key` VARCHAR(100) NOT NULL,
  `meta_value` JSON NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`holding_id`) REFERENCES `holdings` (`id`) ON DELETE CASCADE
);
```

---

## Usage

1. Take **screenshots of your investments** (bank accounts, stocks, FDs, mutual funds, ETFs, etc.).
2. Paste the screenshots into ChatGPT along with this prompt:

```
From the screenshots I provide, generate a single JSON array where:

- Each object has keys: asset_name, asset_type, institution, current_value, currency, updated_at
- Include a "meta" object with key-value pairs (like units, avg_buy_price, invested_value, account_number, isin, etc.)
- updated_at should always be today’s date (YYYY-MM-DD)
- Output valid JSON only (no extra text)

Example:

[
  {
    "asset_name": "HDFC Flexi Cap Fund",
    "asset_type": "Mutual Fund",
    "institution": "HDFC AMC",
    "current_value": 120000.50,
    "currency": "INR",
    "updated_at": "2025-09-13",
    "meta": {
      "units": "450.23",
      "avg_buy_price": "265.50",
      "invested_value": "119500.00",
      "account_number": "123456789",
      "isin": "INF179KC1GH5"
    }
  }
]
```

3. Save the response as `holdings.json`.
4. Run the importer:

```bash
python src/import_holdings.py holdings.json
```

This will:
- Clear old snapshot
- Insert fresh holdings + metadata

---

## 🚀 Launch the Dashboard

To view and analyze your portfolio:
```bash
streamlit run app.py
```
Then open the link shown in your terminal (typically [http://localhost:8501](http://localhost:8501)).

---

## 📝 Notes

- Never commit your personal `holdings.json` to git.  
- `.gitignore` already excludes `*.json` and `.env`.  
- Each run replaces the previous snapshot (fresh state).

---

✅ With this setup you can snapshot your finances anytime and keep a clean normalized database behind it.
