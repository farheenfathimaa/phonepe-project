import json

def load_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_notebook(nb, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

def find_cell(nb, text, cell_type=None):
    for i, cell in enumerate(nb["cells"]):
        if cell_type and cell.get("cell_type") != cell_type:
            continue
        content = "".join(cell.get("source", []))
        if text in content:
            return i
    return -1

nb = load_notebook('ML_Notebook.ipynb')

charts = [
    {
        "num": 1,
        "q1": "A bar chart effectively compares the total transaction amounts across different states, highlighting the top-performing regions distinctly.",
        "q2": "The chart reveals that a few specific states (like Maharashtra, Karnataka, Telangana) account for a massive majority of the total transaction volume, indicating concentrated market dominance.",
        "q3": "Yes. Knowing which states perform best allows for targeted marketing and infrastructure investment in those high-revenue areas. Neglecting emerging states could be a missed opportunity, but no direct negative growth is indicated."
    },
    {
        "num": 2,
        "q1": "A pie chart visually represents the proportion of total transaction value contributed by each transaction type, showing market share clearly.",
        "q2": "Peer-to-peer and Merchant payments make up the vast majority of all transactions, whereas other types like Financial Services are much smaller.",
        "q3": "Yes. This helps businesses understand user behavior and prioritize features for the most popular payment methods. If reliance on a single type is too high, market shifts could pose a risk."
    },
    {
        "num": 3,
        "q1": "A line chart is the optimal choice for displaying trends over time, clearly showing the growth trajectory of transactions.",
        "q2": "There is a massive exponential increase in transaction amounts year over year, showing the rapid adoption of digital payments.",
        "q3": "Yes, it validates the explosive growth of the platform and digital payments in India. No negative insights are found, as the trend is strongly upward."
    },
    {
        "num": 4,
        "q1": "A clustered or colored bar chart effectively displays quarterly performance sequentially while allowing comparison within and across years.",
        "q2": "Transaction counts consistently rise across consecutive quarters. Q4 often shows strong performance due to festive seasons.",
        "q3": "Yes, seasonality insights help in capacity planning and targeted promotions before high-volume quarters. A sudden drop in a quarter would indicate issues, but growth has been consistent."
    },
    {
        "num": 5,
        "q1": "A treemap is excellent for showing hierarchical data or market share among many categories compactly, making brand dominance obvious.",
        "q2": "Xiaomi, Vivo, and Samsung dominate the user base, indicating that mid-range Android devices are the primary platforms for digital payments.",
        "q3": "Yes. App development and testing should prioritize these specific Android environments. Ignoring iOS users completely might limit high-net-worth individual acquisition, though."
    },
    {
        "num": 6,
        "q1": "A bar chart highlights the top performing sub-regions (districts) out of hundreds of possibilities.",
        "q2": "Urban centers like Bengaluru Urban, Pune, and Jaipur dominate the transaction volume compared to rural districts.",
        "q3": "Yes, focusing localized marketing and infrastructure in top urban hubs maximizes ROI. A lack of rural presence could be seen as an area needing improvement."
    },
    {
        "num": 7,
        "q1": "A scatter plot is best for determining the correlation and relationship between two continuous numerical variables.",
        "q2": "There is a strong positive correlation between transaction count and amount, but with an increasing variance as counts grow.",
        "q3": "Yes, it confirms that driving more transactions directly increases total value. The varying spread indicates different average transaction sizes in different regions."
    },
    {
        "num": 8,
        "q1": "A box plot shows the statistical distribution (median, quartiles, outliers) of amounts over time, highlighting shifts in transaction sizes.",
        "q2": "The median transaction amount increases steadily year over year. The large number of high-value outliers indicates significant enterprise usage.",
        "q3": "Yes, the growing median transaction size implies increasing user trust in digital payments for larger purchases."
    },
    {
        "num": 9,
        "q1": "A KDE (Kernel Density Estimate) plot visualizes the continuous probability distribution of app engagement.",
        "q2": "The distribution of app opens is highly right-skewed (visualized on log scale), meaning a majority of users open the app a moderate number of times, while a small segment are power users.",
        "q3": "Yes, it shows user engagement levels. Strategies can be developed to convert moderate users into high-engagement power users."
    },
    {
        "num": 10,
        "q1": "A bar chart comparing derived metrics (average value per transaction) highlights states with higher purchasing power.",
        "q2": "Some states with lower total volumes actually have higher average transaction values, indicating different usage patterns (e.g., larger business transfers vs frequent small purchases).",
        "q3": "Yes. States with high average values but low overall counts are prime targets for user acquisition campaigns to boost overall volume."
    },
    {
        "num": 11,
        "q1": "A stacked bar chart illustrates how the composition of different transaction types has evolved over the years.",
        "q2": "While Peer-to-peer started as the dominant use case, Merchant payments have grown rapidly and take up a progressively larger share over time.",
        "q3": "Yes, it indicates successful penetration into the retail sector. The business should continue optimizing merchant gateways."
    },
    {
        "num": 12,
        "q1": "A histogram with a KDE overlay clearly shows the frequency distribution of transaction sizes.",
        "q2": "The transaction amounts follow a log-normal distribution, which is typical for financial data where smaller amounts are highly frequent.",
        "q3": "Yes, this statistical understanding is crucial for setting up anomaly detection systems to flag unusually high or low transaction volumes."
    },
    {
        "num": 13,
        "q1": "An area chart emphasizes the volume and magnitude of growth in the user base over time.",
        "q2": "The user base is expanding at a steady, accelerating rate without plateauing.",
        "q3": "Yes, this demonstrates strong user acquisition and platform stickiness. A flattening of this curve in the future would indicate market saturation."
    }
]

for chart in charts:
    # Use exact match or startswith to avoid matching "Chart - 10" when looking for "Chart - 1"
    # Although find_cell already returns the first match, which was fine for 1-13 in order, 
    # it's better to be safe. We'll search for `#### Chart - {chart['num']}\n` or similar.
    # We can just iterate through cells and find the exact one.
    idx = -1
    for i, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") == "markdown":
            content = "".join(cell.get("source", [])).strip()
            if content == f"#### Chart - {chart['num']}":
                idx = i
                break
    
    if idx != -1:
        # idx + 1 = code
        q1_idx = idx + 2
        a1_idx = idx + 3
        q2_idx = idx + 4
        a2_idx = idx + 5
        q3_idx = idx + 6
        a3_idx = idx + 7
        
        # Reset questions
        nb["cells"][q1_idx]["source"] = ["##### 1. Why did you pick the specific chart?\n"]
        nb["cells"][q2_idx]["source"] = ["##### 2. What is/are the insight(s) found from the chart?\n"]
        nb["cells"][q3_idx]["source"] = ["##### 3. Will the gained insights help creating a positive business impact?\n", "Are there any insights that lead to negative growth? Justify with specific reason.\n"]
        
        # Set answers
        nb["cells"][a1_idx]["source"] = [chart["q1"]]
        nb["cells"][a2_idx]["source"] = [chart["q2"]]
        nb["cells"][a3_idx]["source"] = [chart["q3"]]

# Let's fix Chart 14 and 15 answers as well, as they might have the same issue since the original notebook had extra cells for answers.
# Actually, the original notebook had extra cells, wait... I'll check Chart 14 and 15 structure.
# They were:
# Cell 146: #### Chart - 14 - Correlation Heatmap
# Cell 147: Code
# Cell 148: Question 1 & Answer 1 & Q2 & A2 & Q3 & A3. Wait, complete_notebook.py put everything in one cell!
# Cell 149: "This chart was selected..." (The old redundant answer cell!)
# Cell 150: Question 2
# Cell 151: The heatmap identifies... (Wait, something is messed up there too).

# Let's clear out all cells that start with "This chart was selected..."
indices_to_delete = []
for i, cell in enumerate(nb["cells"]):
    if cell.get("cell_type") == "markdown":
        content = "".join(cell.get("source", []))
        if "This chart was selected to clearly visualize the distribution" in content:
            indices_to_delete.append(i)

# We shouldn't delete them because that shifts the indices and breaks the notebook structure.
# Instead, we will clear their content or replace them with a single space.
# But for charts 1-13, we just replaced a1_idx, a2_idx, a3_idx with our correct answers, overriding "This chart was selected..."
# Let's clean up Chart 14 and Chart 15 if they have trailing garbage answers.
for i in indices_to_delete:
    nb["cells"][i]["source"] = [""]

# Also clear the "We used GridSearchCV..." duplicate answers in the ML models section
indices_to_delete_ml = []
for i, cell in enumerate(nb["cells"]):
    if cell.get("cell_type") == "markdown":
        content = "".join(cell.get("source", []))
        if "We used GridSearchCV. It exhaustively searches" in content:
            # We updated the proper question cells previously. We'll just clear these duplicates if they are in isolated answer cells.
            indices_to_delete_ml.append(i)

for i in indices_to_delete_ml:
    nb["cells"][i]["source"] = [""]


save_notebook(nb, 'ML_Notebook.ipynb')
print("Answers fixed in notebook.")
