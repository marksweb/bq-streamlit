# bq-streamlit

A test to get BigQuery data in a streamlit app.

Currently not running with Big Query but able to query tavily using GPT with Pydantic AI models.

Copy `.env-example` to `.env` and add your OpenAI and Tavily API keys.

To run, use uv to install dependencies and run `streamlit run app.py`


## Big Query integration

To integrate BQ, you can create a `.streamlit/secrets.toml` file with the following content:

```toml
[gcp_service_account]
type = "service_account"
project_id = "xxx"
private_key_id = "xxx"
private_key = "xxx"
client_email = "xxx"
client_id = "xxx"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "xxx"
```

The details for this can be taken from the JSON credentials generated through IAM
