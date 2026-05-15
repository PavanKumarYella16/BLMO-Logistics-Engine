# 📑 Daily Project Status & Developer Journal
**Project:** Logistics Data Engine (Master's Thesis)
**Developer:** Pavan Kumar Yella

---

## 🗓️ Session 1: Pipeline Foundation & Automation
**Date:** May 15, 2026

### 1. 🏗️ The Infrastructure (The "Where")
* **VS Code:** Set up as the primary coding environment.
* **Virtual Environment (.venv):** Created a private "bubble" to install `pandas` (for data) and `matplotlib` (for charts) so they don't mess up other computer settings.
* **Terminal:** Learned to use the command line to run the code (`python main.py`) and talk to GitHub.

### 2. 🐍 The Python Engine (The "How")
We built the `main.py` using a professional **ETL** structure:

* **Extraction (`load_data`):** Python opens `data/shipments.csv`. It converts the text file into a "DataFrame" (a digital table Python can read).
* **Validation (`validate_data`):** We added a "Cleaner." It automatically deletes rows with negative weights or missing cities. 
    * *Why?* To prevent errors in the final thesis report.
* **Transformation (`transform_logistics_data`):** We added logic. 
    * *Logic:* If weight > 500kg, assign 'High Priority'. Otherwise, 'Standard'.
* **Analysis (`calculate_kpis`):** Python calculates the Average, Max, and Count of shipments.
* **Visualization (`create_visuals`):** Uses the `matplotlib` library to draw a bar chart and save it as `shipment_chart.png`.

### 3. ☁️ The Cloud Backup (The "Safe-Keep")
We connected the local project to **GitHub** to ensure the thesis is never lost.
* **git init:** Started tracking the folder.
* **git remote add:** Linked the laptop folder to the GitHub URL.
* **git pull:** Synchronized the online README with the local code.
* **git push:** Uploaded `main.py` and the data folder to the cloud.

---

## 🚀 How the Application Runs (Step-by-Step)
1.  **Input:** You place a CSV file in the `/data` folder.
2.  **Trigger:** You type `python main.py` in the terminal.
3.  **Process:** * Python loads the data.
    * It scrubs away bad data (Validation).
    * It labels shipments by priority (Transformation).
    * It calculates statistics (KPIs).
4.  **Output:** * The terminal prints a summary report.
    * A new image file `shipment_chart.png` is created/updated.