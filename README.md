[![Language: PL](https://img.shields.io/badge/Language-PL-white.svg)](README_PL.md)

# PharmacyCare 💊

A pharmacy management system built with Python and the Tkinter graphical interface. 
The application allows managing drug inventory, customer databases, and viewing operation statistics.

## ✨ Key Features

- **Authorization:** Role-based access control for Administrator, Pharmacist, and Customer.
- **Inventory Management:** View, search, add, and edit medications (Excel/CSV integration).
- **Customer Database:** Manage customer profiles, including purchase history and address details.
- **Dashboard:** Visualization of key performance indicators (total products, low stock alerts).

## 📂 Project Structure
main.py — Application entry point.

src/gui/ — Graphical user interface (screens, components, styles).

src/services/ — Business logic and data managers.

database/ — Data storage in .xlsx and .csv formats.

assets/ — Fonts.

## 🛠 Tech Stack
Language: Python 3.10

GUI: Tkinter + ttkbootstrap

Data Handling: Pandas, Openpyxl

Styling: Custom fonts (DM Sans) and color themes.

## 📝 Developers
- **Maksim Pyshynski (@Ksar1X)** — Lead Developer: GUI Design, Business Logic, Application Architecture and Backend Logic.
- **Ervin Senkevich (@Ervin581)** — Data Engineer: Database Structure (Excel/CSV), Data Management, and Backend Logic.
- **Arseni Zuyevich (@seniu213)** - Backend Contributor: Data Logic

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.10 or higher installed.

### Installation
Clone the repository and install the required libraries:
```bash
git clone [https://github.com/ksar1x/pharmacy.git](https://github.com/ksar1x/pharmacy.git)
cd pharmacy
pip install -r requirements.txt
