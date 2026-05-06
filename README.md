# PhonePe Transaction Insights

## Project Overview
This project is an end-to-end data science pipeline that extracts data from the PhonePe Pulse GitHub repository, transforms it, loads it into a MySQL database, and visualizes the insights using an interactive Streamlit dashboard. It also includes comprehensive Exploratory Data Analysis (EDA) and Machine Learning (ML) predictive modeling using Jupyter Notebooks.

## Technologies Used
- **Python 3.x**
- **Data Manipulation:** pandas, numpy
- **Data Visualization:** matplotlib, seaborn, plotly, folium
- **Database:** MySQL, sqlalchemy, mysql-connector-python
- **Machine Learning:** scikit-learn, xgboost, joblib, shap
- **Web App / Dashboard:** Streamlit, streamlit-option-menu
- **Version Control:** Git, gitpython, PyGithub

## Features
1. **Data Extraction:** Automated cloning and parsing of PhonePe Pulse JSON data.
2. **Database Schema:** Structured MySQL schema with 9 tables matching PhonePe Pulse categories.
3. **EDA Notebook:** In-depth exploratory data analysis with various visualizations and business insights.
4. **ML Notebook:** Machine learning models (Random Forest, XGBoost, Linear Regression) predicting transaction behavior with hyperparameter tuning.
5. **Streamlit Dashboard:** Interactive application with multiple pages for analyzing transactions, users, insurance, and top performers.
6. **Automated GitHub Deployment:** Script to programmatically push the completed project to a new GitHub repository.

## Step-by-Step Setup Instructions

### 1. Install Requirements
Create a virtual environment (optional but recommended) and install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Database Credentials
Edit the `config.py` file to include your MySQL credentials:
```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "phonepe_pulse"
```

### 3. Setup Database Schema
Run the provided SQL script in your MySQL environment to create the database and tables:
```sql
SOURCE sql_schema.sql;
```
Alternatively, copy the contents of `sql_schema.sql` into your MySQL workbench and execute.

### 4. Run Data Extraction
Execute the data extraction script to clone the PhonePe repository, parse the JSON files, and load the data into your MySQL database. This will take a few minutes.
```bash
python data_extraction.py
```

### 5. Explore Jupyter Notebooks
Run Jupyter Notebook or JupyterLab to view the analysis and machine learning models.
```bash
jupyter notebook
```
- Open `EDA_Notebook.ipynb` to view the Exploratory Data Analysis. Fill in the Markdown "Answer Here" cells with your own observations.
- Open `ML_Notebook.ipynb` to view the Machine Learning pipeline.

### 6. Launch the Streamlit Dashboard
Run the Streamlit application to interact with the visualizations:
```bash
streamlit run app.py
```

### 7. Upload to GitHub
To push your project to a new GitHub repository automatically, run the setup script. It will ask for your GitHub Personal Access Token if it isn't in an `access-token.txt` file or environment variable.
```bash
python setup_github_repo.py
```

## Dataset Reference
- [PhonePe Pulse Data Repository](https://github.com/PhonePe/pulse)
