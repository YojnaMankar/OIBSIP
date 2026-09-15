# OASIS INFOBYTE — Python Programming Internship
## Task 2: BMI Calculator (Advanced)

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-Tkinter%20%26%20TTK-teal.svg)](https://docs.python.org/3/library/tkinter.html)
[![Database](https://img.shields.io/badge/Database-SQLite3-green.svg)](https://www.sqlite.org/)
[![Visualization](https://img.shields.io/badge/Analytics-Matplotlib-orange.svg)](https://matplotlib.org/)

---

## 📌 Project Overview & Objective
This project is developed as part of the **OASIS INFOBYTE SIP Internship (Python Programming Domain)** for **Task 2: BMI Calculator (Advanced)**.

The objective of this application is to deliver a complete, professional-grade desktop GUI tool that calculates Body Mass Index (BMI), categorizes weight status according to World Health Organization (WHO) standards, saves multi-user historical health records in an integrated SQLite database, and generates interactive historical trend analytics charts using Matplotlib.

---

## ✨ Key Features

1. **Modern Professional GUI**:
   - Polished, responsive layout built with Tkinter and custom TTK styling.
   - Distinct cards for Input Measurements, WHO Reference Categories, and Instant Health Insights.
   - Tabbed navigation: **Calculator**, **History**, and **Trend Graph**.

2. **Accurate BMI Computation & Health Insights**:
   - Standard formula: $\text{BMI} = \frac{\text{Weight (kg)}}{(\text{Height (m)})^2}$.
   - Rounded to 2 decimal places.
   - Dynamic calculation of the user's recommended healthy weight range ($18.5 - 24.9\ \text{kg/m}^2$).
   - Personalized clinical advice based on category.

3. **WHO Standard Categorization**:
   - 🔵 **Underweight**: $\text{BMI} < 18.5$
   - 🟢 **Normal Weight**: $18.5 \le \text{BMI} \le 24.9$
   - 🟡 **Overweight**: $25.0 \le \text{BMI} \le 29.9$
   - 🔴 **Obese**: $\text{BMI} \ge 30.0$

4. **Multi-User Profile Management**:
   - Supports multiple independent named users (e.g., Yojna, User 2, User 3).
   - Profiles persist across sessions in the SQLite database.
   - Quick selection combobox or inline new user creation.

5. **Integrated SQLite Database Persistence**:
   - Automatically initializes `bmi_records.db` on launch.
   - Zero manual setup required.
   - Stores: Record ID, User Name, Weight, Height, BMI, Category, and Timestamp.
   - Indexed queries for instant retrieval and filtering.

6. **Interactive History Table**:
   - Filter records by specific user or view all users.
   - Color-coded rows matching BMI categories.
   - Delete selected records or clear an entire user's historical log.

7. **Matplotlib Visual Trend Analytics**:
   - Graphical progression of BMI over time.
   - Semi-transparent colored background bands highlighting WHO zones.
   - Value callout annotations on data points.
   - Interactive zoom, pan, save image toolbar.
   - Handles edge cases gracefully (zero records or single entry).

8. **Bulletproof Input Validation & Error Handling**:
   - Rejects empty, non-numeric, negative, or zero inputs with friendly dialogs.
   - Detects accidental centimeter inputs ($> 3.0$) and advises the user to use meters.
   - Catches all database and visualization exceptions without crashing.

---

## 🛠 Technologies & Libraries Used

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Core programming language |
| **Tkinter / TTK** | Graphical User Interface & Widgets |
| **SQLite3** | Embedded relational database persistence |
| **Matplotlib** | Data visualization & interactive trend plotting |
| **Unittest** | Automated verification and regression test suite |

---

## 📂 Project Directory Structure

```
BMI_Calculator_Advanced/
│
├── main.py              # Application entry point, Tkinter GUI, event handlers
├── database.py          # SQLite database connection, schema setup, CRUD operations
├── bmi_logic.py         # Pure BMI math calculations, WHO categories, input validation
├── test_bmi.py          # Comprehensive automated unit test suite (14 test cases)
├── requirements.txt     # External dependencies (matplotlib)
├── README.md            # Complete project documentation & setup guide
├── bmi_records.db       # Local SQLite database (created automatically upon first run)
└── screenshots/         # Application visual previews
```

---

## 🚀 Installation & Setup Instructions

### 1. Prerequisites
Ensure **Python 3.8+** is installed on your Windows system. Verify in Command Prompt or PowerShell:
```powershell
python --version
```

### 2. Navigate to the Project Folder
```powershell
cd c:\Users\hp\Desktop\oasis\BMI_Calculator_Advanced
```

### 3. Create & Activate Virtual Environment (Recommended)
```powershell
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 🖥 How to Run the Application

Execute the following command in PowerShell / VS Code Terminal:
```powershell
python main.py
```

### Run Automated Unit Tests
To run the automated test suite verifying all math, validation, and database operations:
```powershell
python test_bmi.py
```

---

## 🗄 Database Schema & Details

The database file `bmi_records.db` is stored locally in the project root directory.

```sql
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi REAL NOT NULL,
    category TEXT NOT NULL,
    date_time TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_bmi_user ON bmi_records (user_name);
```

---

## 📸 Screenshots

*(Place your application screenshots in the `screenshots/` directory)*

- **Calculator View**: Input form, WHO category indicators, and instant results card.
- **History View**: Filterable multi-user records table with delete options.
- **Trend View**: Matplotlib visual progression graph with WHO health zones.

---

## 🎯 OASIS INFOBYTE Task Mapping

| Requirement Specified by OASIS | Implementation Status | Implementation Details |
|---|:---:|---|
| Modern Clean GUI | ✅ Completed | Built with custom TTK clamshell styling, responsive cards, and color badges. |
| Proper Inputs (Name, Weight, Height) | ✅ Completed | Form with User selector/entry, weight in kg, height in meters. |
| Calculate, Reset, History, Graph Buttons | ✅ Completed | All buttons implemented and functional with zero placeholders. |
| Accurate BMI Formula | ✅ Completed | $\text{BMI} = \text{weight} / (\text{height}^2)$, rounded to 2 decimal places. |
| 4 WHO Categories | ✅ Completed | Underweight, Normal, Overweight, Obese with color badges and advice. |
| Input Validation & Error Handling | ✅ Completed | Rejects empty, non-numeric, negative, and zero values; catches cm vs m. |
| Multi-User Support | ✅ Completed | Dedicated dropdown, individual record isolation, multi-user tracking. |
| SQLite Persistence | ✅ Completed | Auto-created `bmi_records.db`, parameterized queries, indexed retrieval. |
| Historical Records View | ✅ Completed | Interactive Treeview with user filter, deletion, and record counters. |
| Matplotlib Trend Graph | ✅ Completed | Embedded figure canvas with WHO color zones, points, annotations, and toolbar. |

---

## 🔮 Future Enhancements
- Export historical BMI records to CSV and PDF clinical reports.
- Support body fat percentage calculation using caliper or navy tape measurements.
- Daily water intake and caloric maintenance estimators based on activity level.
