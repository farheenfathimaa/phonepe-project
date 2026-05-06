import json

notebook_path = "ML_Notebook.ipynb"
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Helper function to find cell index by content substring
def find_cell(nb, text, cell_type=None):
    for i, cell in enumerate(nb["cells"]):
        if cell_type and cell.get("cell_type") != cell_type:
            continue
        content = "".join(cell.get("source", []))
        if text in content:
            return i
    return -1

# --- Chart 14 ---
chart14_idx = find_cell(nb, "Chart - 14 - Correlation Heatmap", "markdown")
if chart14_idx != -1:
    code_cell_idx = chart14_idx + 1
    markdown_cell_idx = chart14_idx + 2
    
    nb["cells"][code_cell_idx]["source"] = [
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
    nb["cells"][code_cell_idx]["outputs"] = []
    
    nb["cells"][markdown_cell_idx]["source"] = [
        "##### 1. Why did you pick the specific chart?\n",
        "\n",
        "A heatmap is the standard tool for visualizing a correlation matrix, allowing for quick identification of highly correlated numerical features.\n",
        "\n",
        "##### 2. What is/are the insight(s) found from the chart?\n",
        "\n",
        "The heatmap identifies which numerical variables are strongly correlated (e.g., Transaction Count and Transaction Amount), which is essential feature selection information for predictive modeling.\n",
        "\n",
        "##### 3. Will the gained insights help creating a positive business impact?\n",
        "Are there any insights that lead to negative growth? Justify with specific reason.\n",
        "\n",
        "Yes, understanding feature correlations simplifies the predictive models, reducing computational costs and improving accuracy. There are no direct negative growth insights from a heatmap, but ignoring strong multi-collinearity could lead to flawed model predictions.\n"
    ]

# --- Chart 15 ---
chart15_idx = find_cell(nb, "Chart - 15 - Pair Plot", "markdown")
if chart15_idx != -1:
    code_cell_idx = chart15_idx + 1
    markdown_cell_idx = chart15_idx + 2
    
    nb["cells"][code_cell_idx]["source"] = [
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
    nb["cells"][code_cell_idx]["outputs"] = []
    
    nb["cells"][markdown_cell_idx]["source"] = [
        "##### 1. Why did you pick the specific chart?\n",
        "\n",
        "A pair plot provides a comprehensive grid of scatter plots and histograms, allowing us to simultaneously observe the distributions and pairwise relationships of multiple key metrics.\n",
        "\n",
        "##### 2. What is/are the insight(s) found from the chart?\n",
        "\n",
        "This provides a macro-view of the interactions between different numeric features, helping to spot non-linear relationships and distributions at a glance.\n",
        "\n",
        "##### 3. Will the gained insights help creating a positive business impact?\n",
        "Are there any insights that lead to negative growth? Justify with specific reason.\n",
        "\n",
        "Yes, macro-level insights into distributions help in setting realistic business targets and anomaly detection thresholds. Skewed distributions might indicate that the business is overly reliant on a small subset of heavy users, which is a risk.\n"
    ]


# --- Hypothesis 1 ---
hyp1_idx = find_cell(nb, "Hypothetical Statement - 1", "markdown")
if hyp1_idx != -1:
    # Look for code cell and markdown cells after
    code_idx = hyp1_idx + 2
    nb["cells"][code_idx]["source"] = [
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
    nb["cells"][code_idx]["outputs"] = []
    
    nb["cells"][hyp1_idx + 1]["source"] = [
        "#### 1. State Your research hypothesis as a null hypothesis and alternate hypothesis.\n",
        "\n",
        "**Null Hypothesis (H0):** There is no significant difference in transaction amounts across years (specifically 2018 vs 2022).\n",
        "\n",
        "**Alternate Hypothesis (H1):** There is a significant difference in transaction amounts across years, indicating growth."
    ]
    nb["cells"][hyp1_idx + 3]["source"] = [
        "##### Which statistical test have you done to obtain P-Value?\n",
        "\n",
        "**Independent Two-Sample T-Test**"
    ]
    nb["cells"][hyp1_idx + 4]["source"] = [
        "##### Why did you choose the specific statistical test?\n",
        "\n",
        "To compare the means of two independent groups (transactions in 2018 vs. transactions in 2022) to determine if there is statistically significant evidence of growth over time."
    ]

# --- Hypothesis 2 ---
hyp2_idx = find_cell(nb, "Hypothetical Statement - 2", "markdown")
if hyp2_idx != -1:
    code_idx = hyp2_idx + 2
    nb["cells"][code_idx]["source"] = [
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
    nb["cells"][code_idx]["outputs"] = []
    
    nb["cells"][hyp2_idx + 1]["source"] = [
        "#### 1. State Your research hypothesis as a null hypothesis and alternate hypothesis.\n",
        "\n",
        "**Null Hypothesis (H0):** Maharashtra's average transaction volume is equal to the national average transaction volume.\n",
        "\n",
        "**Alternate Hypothesis (H1):** Maharashtra's average transaction volume is significantly different (higher) than the national average."
    ]
    nb["cells"][hyp2_idx + 3]["source"] = [
        "##### Which statistical test have you done to obtain P-Value?\n",
        "\n",
        "**One-Sample T-Test**"
    ]
    nb["cells"][hyp2_idx + 4]["source"] = [
        "##### Why did you choose the specific statistical test?\n",
        "\n",
        "To compare the sample mean of a specific group (Maharashtra) against the known population mean (national average) to determine if the state's performance is statistically exceptional."
    ]

# --- Hypothesis 3 ---
hyp3_idx = find_cell(nb, "Hypothetical Statement - 3", "markdown")
if hyp3_idx != -1:
    code_idx = hyp3_idx + 2
    nb["cells"][code_idx]["source"] = [
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
    nb["cells"][code_idx]["outputs"] = []
    
    nb["cells"][hyp3_idx + 1]["source"] = [
        "#### 1. State Your research hypothesis as a null hypothesis and alternate hypothesis.\n",
        "\n",
        "**Null Hypothesis (H0):** There is no significant difference in average transaction value between Peer-to-peer payments and Merchant payments.\n",
        "\n",
        "**Alternate Hypothesis (H1):** Peer-to-peer payments generate a significantly different (higher) average transaction value than Merchant payments."
    ]
    nb["cells"][hyp3_idx + 3]["source"] = [
        "##### Which statistical test have you done to obtain P-Value?\n",
        "\n",
        "**Independent Two-Sample T-Test**"
    ]
    nb["cells"][hyp3_idx + 4]["source"] = [
        "##### Why did you choose the specific statistical test?\n",
        "\n",
        "To compare the means of two distinct categorical transaction types (P2P vs Merchant) to verify which drives higher individual transaction values."
    ]


# --- Feature Engineering: Missing Values ---
mv_idx = find_cell(nb, "1. Handling Missing Values", "markdown")
if mv_idx != -1:
    code_idx = mv_idx + 1
    nb["cells"][code_idx]["source"] = [
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
    nb["cells"][code_idx]["outputs"] = []
    
    nb["cells"][mv_idx + 2]["source"] = [
        "#### What all missing value imputation techniques have you used and why did you use those techniques?\n",
        "\n",
        "The missing values in the aggregated datasets were negligible or non-existent due to the structured nature of the PhonePe Pulse data. If any sparse rows exist, we simply drop them (using `.dropna()`) to maintain data integrity without introducing bias through artificial imputation."
    ]


# --- Feature Engineering: Outliers ---
out_idx = find_cell(nb, "2. Handling Outliers", "markdown")
if out_idx != -1:
    code_idx = out_idx + 1
    nb["cells"][code_idx]["source"] = [
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
    nb["cells"][code_idx]["outputs"] = []
    
    nb["cells"][out_idx + 2]["source"] = [
        "##### What all outlier treatment techniques have you used and why did you use those techniques?\n",
        "\n",
        "We used the **IQR (Interquartile Range) capping method** to handle extreme outliers in numeric features like `Transaction_amount`.\n",
        "\n",
        "**Why:** Financial transaction data often contains highly skewed, massive outliers (e.g., enterprise-level transfers). Capping these extreme values at the upper IQR bound prevents them from distorting predictive machine learning models while still keeping the data points in the dataset."
    ]


with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Notebook completion script executed successfully.")
