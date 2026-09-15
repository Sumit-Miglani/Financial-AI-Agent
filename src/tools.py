import pandas as pd
import json

def reconcile_ledgers(ledger_1_path: str, ledger_2_path: str) -> str:
    """Reconciles two financial ledger CSVs by stripping 'GTO' key suffixes and identifying discrepancies."""
    df1 = pd.read_csv(ledger_1_path)
    df2 = pd.read_csv(ledger_2_path)
    
    # Sanitize ledger keys by stripping 'GTO' suffix from ERP records
    df1['clean_key'] = df1['ledger_key'].astype(str).str.replace('GTO$', '', regex=True)
    df2['clean_key'] = df2['ledger_key'].astype(str)
    
    # Execute full outer join on clean keys
    merged = pd.merge(df1, df2, on='clean_key', how='outer', suffixes=('_erp', '_audit'))
    
    # Calculate variance
    merged['variance'] = merged['recorded_amount'] - merged['verified_amount']
    discrepancies = merged[merged['variance'] != 0]
    
    return discrepancies[['clean_key', 'account_name_erp', 'recorded_amount', 'verified_amount', 'variance']].to_json(orient='records')
