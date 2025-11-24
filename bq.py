from google.cloud import bigquery
from google.cloud.bigquery import QueryJobConfig


def manifest_to_prompt(schema: dict) -> str:
    parts = [
        f"Project: {schema['project']}",
        f"Dataset: {schema['dataset']}",
        "Tables and columns:",
    ]
    for tbl, cols in schema["tables"].items():
        # Keep it compact; join columns with comma
        col_list = ", ".join(cols)
        parts.append(f"- {tbl}: {col_list}")
    return "\n".join(parts)


def dry_run_sql(client: bigquery.Client, sql: str) -> tuple[bool, str | None]:
    try:
        client.query(
            sql, job_config=QueryJobConfig(dry_run=True, use_query_cache=False)
        )
        # If no exception, dry-run succeeded
        return True, None
    except Exception as e:
        return False, str(e)
