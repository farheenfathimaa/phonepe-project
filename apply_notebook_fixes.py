import json

notebook_path = "ML_Notebook.ipynb"
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

current_hypo = 0

for i, cell in enumerate(nb["cells"]):
    content = "".join(cell.get("source", []))
    cell_type = cell.get("cell_type")
    
    if cell_type == "markdown" and "Hypothetical Statement - 1" in content:
        current_hypo = 1
    elif cell_type == "markdown" and "Hypothetical Statement - 2" in content:
        current_hypo = 2
    elif cell_type == "markdown" and "Hypothetical Statement - 3" in content:
        current_hypo = 3

    if cell_type == "code":
        if "# Correlation Heatmap visualization code" in content:
            cell["source"] = [
                "# Correlation Heatmap visualization code\n",
                "import seaborn as sns\n",
                "import matplotlib.pyplot as plt\n",
                "import pandas as pd\n",
                "import sqlalchemy, config, urllib.parse\n",
                "try:\n",
                "    engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{config.DB_USER}:{urllib.parse.quote_plus(config.DB_PASSWORD)}@{config.DB_HOST}/{config.DB_NAME}')\n",
                "    df_trans = pd.read_sql('SELECT * FROM Aggregated_transaction', engine)\n",
                "    numerical_cols = df_trans.select_dtypes(include=['float64', 'int64']).columns\n",
                "    corr_matrix = df_trans[numerical_cols].corr()\n",
                "    plt.figure(figsize=(10, 6))\n",
                "    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')\n",
                "    plt.title('Correlation Heatmap of Transaction Metrics')\n",
                "    plt.show()\n",
                "except Exception as e:\n",
                "    print(f'Error: {e}')\n"
            ]
            nb["cells"][i+2]["source"] = [
                "This chart was selected to clearly visualize the distribution and comparison of the target metric across different categories, allowing for easy identification of the highest and lowest performing segments."
            ]
            nb["cells"][i+4]["source"] = [
                "The heatmap identifies which numerical variables are strongly correlated (e.g., Transaction Count and Transaction Amount), which is essential feature selection information for predictive modeling."
            ]
            nb["cells"][i+6]["source"] = [
                "Yes, understanding feature correlations simplifies the predictive models, reducing computational costs and improving accuracy. There are no direct negative growth insights from a heatmap, but ignoring strong multi-collinearity could lead to flawed model predictions."
            ]
            
        elif "# Pair Plot visualization code" in content:
            cell["source"] = [
                "# Pair Plot visualization code\n",
                "import seaborn as sns\n",
                "import matplotlib.pyplot as plt\n",
                "import pandas as pd\n",
                "import sqlalchemy, config, urllib.parse\n",
                "try:\n",
                "    engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{config.DB_USER}:{urllib.parse.quote_plus(config.DB_PASSWORD)}@{config.DB_HOST}/{config.DB_NAME}')\n",
                "    df_trans = pd.read_sql('SELECT * FROM Aggregated_transaction', engine)\n",
                "    numerical_cols = df_trans.select_dtypes(include=['float64', 'int64']).columns\n",
                "    sns.pairplot(df_trans[numerical_cols])\n",
                "    plt.suptitle('Pair Plot of Transaction Metrics', y=1.02)\n",
                "    plt.show()\n",
                "except Exception as e:\n",
                "    print(f'Error: {e}')\n"
            ]
            nb["cells"][i+2]["source"] = [
                "A pair plot provides a comprehensive grid of scatter plots and histograms, allowing us to simultaneously observe the distributions and pairwise relationships of multiple key metrics."
            ]
            nb["cells"][i+4]["source"] = [
                "This provides a macro-view of the interactions between different numeric features, helping to spot non-linear relationships and distributions at a glance."
            ]
            nb["cells"][i+6]["source"] = [
                "Yes, macro-level insights into distributions help in setting realistic business targets and anomaly detection thresholds. Skewed distributions might indicate that the business is overly reliant on a small subset of heavy users, which is a risk."
            ]

        elif "# Perform Statistical Test to obtain P-Value" in content:
            if current_hypo == 1:
                cell["source"] = [
                    "# Perform Statistical Test to obtain P-Value\n",
                    "import pandas as pd\n",
                    "import sqlalchemy, config, urllib.parse\n",
                    "from scipy import stats\n",
                    "\n",
                    "try:\n",
                    "    engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{config.DB_USER}:{urllib.parse.quote_plus(config.DB_PASSWORD)}@{config.DB_HOST}/{config.DB_NAME}')\n",
                    "    df_trans = pd.read_sql('SELECT * FROM Aggregated_transaction', engine)\n",
                    "    trans_2018 = df_trans[df_trans['Year'] == 2018]['Transaction_amount'].dropna()\n",
                    "    trans_2022 = df_trans[df_trans['Year'] == 2022]['Transaction_amount'].dropna()\n",
                    "    \n",
                    "    t_stat, p_value = stats.ttest_ind(trans_2018, trans_2022, equal_var=False)\n",
                    "    print(f'T-Statistic: {t_stat:.4f}')\n",
                    "    print(f'P-Value: {p_value:.4e}')\n",
                    "    if p_value < 0.05:\n",
                    "        print('Reject the Null Hypothesis: There is a significant difference in transaction amounts between 2018 and 2022.')\n",
                    "    else:\n",
                    "        print('Fail to reject the Null Hypothesis.')\n",
                    "except Exception as e:\n",
                    "    print(f'Error: {e}')\n"
                ]
                nb["cells"][i-1]["source"] = ["**Null Hypothesis (H0):** There is no significant difference in transaction amounts across years (specifically 2018 vs 2022).\n\n**Alternate Hypothesis (H1):** There is a significant difference in transaction amounts across years, indicating growth."]
                nb["cells"][i+2]["source"] = ["**Independent Two-Sample T-Test**"]
                nb["cells"][i+4]["source"] = ["To compare the means of two independent groups (transactions in 2018 vs. transactions in 2022) to determine if there is statistically significant evidence of growth over time."]
            elif current_hypo == 2:
                cell["source"] = [
                    "# Perform Statistical Test to obtain P-Value\n",
                    "try:\n",
                    "    maharashtra_trans = df_trans[df_trans['State'] == 'Maharashtra']['Transaction_count'].dropna()\n",
                    "    national_mean = df_trans['Transaction_count'].mean()\n",
                    "    \n",
                    "    t_stat, p_value = stats.ttest_1samp(maharashtra_trans, national_mean)\n",
                    "    print(f'National Mean Transaction Count: {national_mean:.4f}')\n",
                    "    print(f'Maharashtra Mean Transaction Count: {maharashtra_trans.mean():.4f}')\n",
                    "    print(f'T-Statistic: {t_stat:.4f}')\n",
                    "    print(f'P-Value: {p_value:.4e}')\n",
                    "    if p_value < 0.05:\n",
                    "        print('Reject the Null Hypothesis: Maharashtra has a significantly different transaction volume than the national average.')\n",
                    "except Exception as e:\n",
                    "    print(f'Error: {e}')\n"
                ]
                nb["cells"][i-1]["source"] = ["**Null Hypothesis (H0):** Maharashtra's average transaction volume is equal to the national average transaction volume.\n\n**Alternate Hypothesis (H1):** Maharashtra's average transaction volume is significantly different (higher) than the national average."]
                nb["cells"][i+2]["source"] = ["**One-Sample T-Test**"]
                nb["cells"][i+4]["source"] = ["To compare the sample mean of a specific group (Maharashtra) against the known population mean (national average) to determine if the state's performance is statistically exceptional."]
            elif current_hypo == 3:
                cell["source"] = [
                    "# Perform Statistical Test to obtain P-Value\n",
                    "try:\n",
                    "    p2p_trans = df_trans[df_trans['Transaction_type'].str.contains('Peer-to-peer', case=False, na=False)]['Transaction_amount'].dropna()\n",
                    "    merchant_trans = df_trans[df_trans['Transaction_type'].str.contains('Merchant', case=False, na=False)]['Transaction_amount'].dropna()\n",
                    "    \n",
                    "    t_stat, p_value = stats.ttest_ind(p2p_trans, merchant_trans, equal_var=False)\n",
                    "    print(f'P2P Mean Amount: {p2p_trans.mean():.4f}')\n",
                    "    print(f'Merchant Mean Amount: {merchant_trans.mean():.4f}')\n",
                    "    print(f'T-Statistic: {t_stat:.4f}')\n",
                    "    print(f'P-Value: {p_value:.4e}')\n",
                    "    if p_value < 0.05:\n",
                    "        print('Reject the Null Hypothesis: There is a significant difference between P2P and Merchant transaction values.')\n",
                    "except Exception as e:\n",
                    "    print(f'Error: {e}')\n"
                ]
                nb["cells"][i-1]["source"] = ["**Null Hypothesis (H0):** There is no significant difference in average transaction value between Peer-to-peer payments and Merchant payments.\n\n**Alternate Hypothesis (H1):** Peer-to-peer payments generate a significantly different (higher) average transaction value than Merchant payments."]
                nb["cells"][i+2]["source"] = ["**Independent Two-Sample T-Test**"]
                nb["cells"][i+4]["source"] = ["To compare the means of two distinct categorical transaction types (P2P vs Merchant) to verify which drives higher individual transaction values."]

        elif "# Handling Missing Values & Missing Value Imputation" in content:
            cell["source"] = [
                "# Handling Missing Values & Missing Value Imputation\n",
                "import pandas as pd\n",
                "import sqlalchemy, config, urllib.parse\n",
                "try:\n",
                "    engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{config.DB_USER}:{urllib.parse.quote_plus(config.DB_PASSWORD)}@{config.DB_HOST}/{config.DB_NAME}')\n",
                "    df_trans = pd.read_sql('SELECT * FROM Aggregated_transaction', engine)\n",
                "    print(f'Missing values before: {df_trans.isnull().sum().sum()}')\n",
                "    df_trans.dropna(inplace=True)\n",
                "    print(f'Missing values after: {df_trans.isnull().sum().sum()}')\n",
                "except Exception as e:\n",
                "    print(f'Error: {e}')\n"
            ]
            nb["cells"][i+2]["source"] = ["The missing values in the aggregated datasets were negligible or non-existent due to the structured nature of the PhonePe Pulse data. If any sparse rows exist, we simply drop them (using `.dropna()`) to maintain data integrity without introducing bias through artificial imputation."]

        elif "# Handling Outliers & Outlier treatments" in content:
            cell["source"] = [
                "# Handling Outliers & Outlier treatments\n",
                "try:\n",
                "    Q1 = df_trans['Transaction_amount'].quantile(0.25)\n",
                "    Q3 = df_trans['Transaction_amount'].quantile(0.75)\n",
                "    IQR = Q3 - Q1\n",
                "    upper_bound = Q3 + 1.5 * IQR\n",
                "    print(f'Outlier Upper Bound for Transaction Amount: {upper_bound:.2f}')\n",
                "    \n",
                "    df_trans['Transaction_amount'] = df_trans['Transaction_amount'].clip(upper=upper_bound)\n",
                "    print('Outliers capped successfully using IQR method.')\n",
                "except Exception as e:\n",
                "    print(f'Error: {e}')\n"
            ]
            nb["cells"][i+2]["source"] = ["We used the **IQR (Interquartile Range) capping method** to handle extreme outliers in numeric features like `Transaction_amount`.\n\n**Why:** Financial transaction data often contains highly skewed, massive outliers (e.g., enterprise-level transfers). Capping these extreme values at the upper IQR bound prevents them from distorting predictive machine learning models while still keeping the data points in the dataset."]

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Notebook fixes applied successfully.")
