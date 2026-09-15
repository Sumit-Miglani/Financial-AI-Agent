import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("data", exist_ok=True)

# 1. SEC API Configuration
CIK = "0001652044"  # Alphabet Inc. (Google)
url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json"
headers = {'User-Agent': 'CloudAIEngineerProject sumit@example.com'}

print("Fetching live SEC EDGAR balance sheet facts for Alphabet Inc...")
response = requests.get(url, headers=headers)

if response.status_code != 200:
    raise Exception(f"Failed to fetch SEC data: HTTP {response.status_code}")

data = response.json()
us_gaap = data['facts']['us-gaap']

# Key SEC Balance Sheet Concepts
metrics_to_extract = [
    'Assets',
    'Liabilities',
    'StockholdersEquity',
    'CashAndCashEquivalentsAtCarryingValue',
    'PropertyPlantAndEquipmentNet'
]

sec_records = []
for idx, metric in enumerate(metrics_to_extract, start=1001):
    if metric in us_gaap:
        units = us_gaap[metric]['units']
        unit_key = 'USD' if 'USD' in units else list(units.keys())[0]
        # Grab the latest reported filing value
        latest_fact = units[unit_key][-1]
        val = float(latest_fact['val'])
        sec_records.append({
            'account_id': f"ACC{idx}",
            'account_name': metric,
            'amount': val
        })

df_base = pd.DataFrame(sec_records)

# 2. Generate Primary Internal ERP Ledger (With 'GTO' key suffix)
df_erp = df_base.copy()
df_erp['ledger_key'] = df_erp['account_id'] + "GTO"
df_erp['recorded_amount'] = df_erp['amount']
df_erp[['ledger_key', 'account_name', 'recorded_amount']].to_csv('data/financial_1.csv', index=False)

# 3. Generate External Audit Ledger (Clean keys, with 1 introduced discrepancy)
df_audit = df_base.copy()
df_audit['ledger_key'] = df_audit['account_id']
df_audit['verified_amount'] = df_audit['amount']
# Introduce $50M audit adjustment on Cash
df_audit.loc[df_audit['account_name'] == 'CashAndCashEquivalentsAtCarryingValue', 'verified_amount'] += 50000000.0
df_audit[['ledger_key', 'account_name', 'verified_amount']].to_csv('data/financial_2.csv', index=False)

print("SEC EDGAR ledgers saved to data/financial_1.csv and data/financial_2.csv")

# 4. Render Visual BI Dashboard Screenshot from SEC Financials
fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('tight')
ax.axis('off')

table_data = [["Metric Name", "Reported Value (USD)"]]
for _, row in df_base.iterrows():
    table_data.append([row['account_name'], f"${row['amount']:,.2f}"])

table = ax.table(cellText=table_data, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.8)

for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor('#0F9D58') # Google Green
        cell.set_text_props(color='white', weight='bold')

plt.title("SEC EDGAR Q3 Balance Sheet Metrics (Alphabet Inc.)", fontsize=13, pad=15, weight='bold')
plt.savefig('data/dashboard_bi.png', bbox_inches='tight', dpi=150)
plt.close()

print("Visual SEC Dashboard screenshot generated in data/dashboard_bi.png")
