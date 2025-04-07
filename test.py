from dfcx_scrapi.tools.evaluations import DataLoader
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
sheet_name = "Agent Evaluation Results"

CREDS_PATH = "/Users/thomas.phipps/.config/gcloud/phipps-agent-test-account.json"

data = DataLoader(
    creds_path=CREDS_PATH
)

# load from google sheets
sheet_name = "Chat_Agent_Tests"
sheet_tab = "shopper"
foo = data.create_sheet(sheet_name)
sample_df = data.from_google_sheets(sheet_name, sheet_tab)


# load from csv
# csv_file_path = "./chat_test.csv"
# sample_df = data.from_csv(csv_file_path)

from dfcx_scrapi.tools.evaluations import Evaluations

# [1] Define your Agent ID here
agent_id = "projects/gcp-kibo-dev/locations/us-central1/agents/31449564-b272-49f3-8246-af265eddb69e" # Example Agent
# [2] Instantiate Evals class w/ Metrics
evals = Evaluations(agent_id, metrics=["response_similarity", "tool_call_quality"])

eval_results = evals.run_query_and_eval(sample_df.head(10))

print(f"Average Similarity {eval_results.similarity.mean()}")
print(f"Average Tool Call Quality {eval_results.tool_name_match.mean()}")


print(eval_results.head())

# from dfcx_scrapi.tools.evaluations import DataLoader
reporting_sheet ='Agent Evaluation Results'
data = DataLoader(
    sheet_name=reporting_sheet,
    creds_path=CREDS_PATH,
)
# data.sheets_client = sheets_service


output_csv_path = "/Users/thomas.phipps/git/proto/dfcx-scrapi/evaluation_results.csv"
eval_results.to_csv(output_csv_path, index=False)



data.write_eval_results_to_sheets(eval_results, reporting_sheet, results_tab="latest_results")
data.append_test_results_to_sheets(eval_results, reporting_sheet, summary_tab="reporting")