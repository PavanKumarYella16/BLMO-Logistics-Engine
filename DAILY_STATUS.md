# 📑 Logistics Data Engine | Developer Journal
**Project:** SmartRoute Dispatcher (Master's Thesis)
**Developer:** Pavan Kumar Yella

---

## 📅 May 15, 2026: Pipeline Foundation & Automation
**Current Focus:** ETL Logic, Data Validation, and Cloud Sync.

### 1. 🏗️ The Infrastructure (The "Where")
* **Virtual Environment (.venv):** Created a private "bubble" for `pandas` and `matplotlib` to ensure stability.
* **Terminal Mastery:** Used CLI for execution (`python main.py`) and version control.

### 2. 🐍 The Python Engine (The "How")
Built `main.py` using a professional **ETL (Extract, Transform, Load)** structure:
* **Extraction:** Python loads `data/shipments.csv` into a DataFrame.
* **Validation:** Automated "Cleaner" removes negative weights or missing cities to ensure Data Integrity.
* **Transformation:** Implemented Priority Logic (Weight > 500kg = 'High Priority').
* **Analysis:** Automated calculation of KPIs (Average, Max, and Count).
* **Visualization:** Generates `shipment_chart.png` automatically using `matplotlib`.

### 3. 🚀 Upcoming Real-World Challenges (Strategic Roadmap)
To reach a Master's Thesis standard, the engine will evolve to solve these industrial "Pain Points":
* **Resource Optimization:** Vehicle-to-Load matching (avoiding under-utilized van space).
* **Dynamic Routing:** Solving the "Last-Mile" density problem in Berlin districts.
* **Sustainability Tracking:** $CO_2$ emission calculations per shipment.
* **Financial Analysis:** "Cost-per-Delivery" metrics for profitability tracking.

---

## 📅 May 14, 2026: Infrastructure & Cloud Integration
**Goal:** Establishing the professional foundation.

### ✅ Completed:
* **Environment:** Configured Python 3.x and VS Code on Windows.
* **Version Control:** Initialized Git and connected to GitHub (`git remote add origin`).
* **Conflict Resolution:** Resolved "unrelated histories" merge error to sync local and cloud README files.
* **Architecture:** Created `/Data` (Inputs) and `/docs` (Technical Archives) directory structure.

---

## ⚙️ How the Application Runs (The Logic Flow)
1. **Input:** Raw `shipments.csv` is placed in `/data`.
2. **Trigger:** `python main.py` executed in terminal.
3. **Process:** Data is scrubbed, prioritized, and analyzed.
4. **Output:** Terminal prints a summary report; `shipment_chart.png` is updated.

---
*Generated for Master of Industrial Engineering & Int. Management | Hochschule Fresenius*