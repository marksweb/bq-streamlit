import asyncio

import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

from agent import run_agent
from bq import manifest_to_prompt, dry_run_sql

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


@st.cache_data(ttl=600)
def get_schema_manifest(_client: bigquery.Client, gameweek: int) -> dict:
    dataset = f"plfpl-production.ism_GW{gameweek}"
    sql = f"""
    SELECT table_name, column_name, data_type
    FROM `{dataset}.INFORMATION_SCHEMA.COLUMNS`
    ORDER BY table_name, ordinal_position
    """
    rows = client.query(sql).result()
    manifest: dict[str, list[str]] = {}
    for r in rows:
        manifest.setdefault(r["table_name"], []).append(r["column_name"])
    return {
        "project": "plfpl-production",
        "dataset": f"ism_GW{gameweek}",
        "tables": manifest,
    }


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query: str):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


st.set_page_config(page_title="BigQuery Assistant", page_icon=" ")
st.title("BigQuery Assistant")
st.write(
    "Ask a question about your data. The assistant will generate BigQuery SQL and run it for the selected Gameweek."
)

gw = st.number_input("Gameweek", min_value=1, max_value=38, value=12, step=1)

query = st.text_input(
    "What would you like to find?",
    "Top 10 most transferred-in players and their counts",
)

sql = None
results_rows = None

if st.button("Run Query"):
    with st.spinner("Generating SQL and querying BigQuery. Please wait..."):
        try:
            schema = get_schema_manifest(client, int(gw))
            schema_text = manifest_to_prompt(schema)

            sql = asyncio.run(run_agent(query, int(gw), schema_text))

            ok, err = dry_run_sql(client, sql)
            if not ok:
                # Try a single self-correction round by telling the agent the error
                correction_prompt = (
                    query
                    + "\n\nNote: Prior SQL failed validation with this BigQuery error. "
                    "Please correct using the provided schema only. Error: "
                    + (err or "")
                )
                sql = asyncio.run(run_agent(correction_prompt, int(gw), schema_text))
                ok2, err2 = dry_run_sql(client, sql)
                if not ok2:
                    raise RuntimeError(err2 or err)

            results_rows = run_query(sql)
        except Exception as e:
            error_msg = str(e)
if sql:
    with st.expander("Show generated SQL"):
        st.code(sql, language="sql")

if results_rows is not None:
    if len(results_rows) == 0:
        st.info("Query returned no rows.")
    else:
        st.success(f"Returned {len(results_rows)} rows")
        st.dataframe(results_rows)
