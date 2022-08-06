import os

import pandas as pd
import requests

from s3 import upload_file

BASE_URL = "https://api.youneedabudget.com/v1"

budget_id = os.environ["BUDGET_ID"]
ynab_api_key = os.environ["YNAB_API_KEY"]

if __name__ == "__main__":
    headers = {"Authorization": f"Bearer {ynab_api_key}"}

    transactions_response = requests.get(
        f"{BASE_URL}/budgets/{budget_id}/transactions", headers=headers
    )

    if not transactions_response.ok:
        raise Exception(transactions_response.text)

    transactions_df = pd.DataFrame(transactions_response.json()["data"]["transactions"])

    st_series = transactions_df["subtransactions"]
    st_series_exploded = st_series.explode()
    subtransactions_df = pd.DataFrame(
        st_series_exploded[st_series_exploded.notna()].tolist()
    )

    del transactions_df["subtransactions"]

    upload_file(transactions_df, "transactions.parquet")
    upload_file(subtransactions_df, "subtransactions.parquet")
