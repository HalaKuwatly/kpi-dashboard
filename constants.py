import datetime

END_DATE = datetime.date.today()

SPRINT_LENGTH = 14

STORY_POINTS_FIELD_NAME = "customfield_10039"
POST_SPRINT_ESTIMATE_FIELD_NAME = "customfield_10118"

JIRA_SERVER = "https://eb7team.atlassian.net/"
JIRA_USERNAME = "hala@e-bot7.com"


NOTION_URL_BASE = "https://www.notion.so/ebot7/{}?v={}"

NOTION_COLLECTION = "6c6ad8f23e374785922082047df57e34"
NOTION_VIEW = "adabccb5cde7410dad8df3140a8bf93d"

TEAM_CONSTANTS = {
    "nlu": {
        "sprint_query": "project in ('NLU Application', 'ML') AND status changed to 'Done' after '{start_date}' before '{end_date}' AND issuetype in (Story, Subtask, Bug, Task)",
        "status_change_query": "project in ('NLU Application', 'ML') AND status changed to 'Done' after '{start_date}' before '{end_date}' AND issuetype in (Story, Subtask, Bug, Task)",
        "statuses": ["In Progress", "Review", "QA"],
        "start_date": datetime.date(2021, 2, 28),
        "start_sprint_id": 52,
        "sprint_start_date": datetime.date(2021, 2, 28),
        "sprint_name": "Sprint {sprint_id}",
    },
    "ce": {
        "sprint_query": "project in ('CE') AND sprint in ('{sprint_id}')",
        "status_change_query": "project = 'CE' AND status changed to ('In Progress', 'Review', 'Merged') after '{start_date}' before '{end_date}'",
        "statuses": ["In Progress", "Review", "Merged"],
        "start_date": datetime.date(2021, 1, 1),
        "start_sprint_id": 7,
        "sprint_start_date": datetime.date(2021, 2, 15),
        "sprint_name": "CE Sprint {sprint_id}",
    },
}
