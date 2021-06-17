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
        "sprint_start_date": datetime.date(2021, 3, 29),
        "start_sprint_id": 54,
        "members": [
            "ivan",
            "buddhi",
            "hala",
            "sumit",
            "hai",
            "manuel",
            "till",
            "jinay",
        ],
        "to_do_status": ["To Do", "Selected for Development"],
    },
    "apps": {
        "sprint_query": "project in ('NLU Application') AND status changed to 'Done' after '{start_date}' before '{end_date}' AND issuetype in (Story, Subtask, Bug, Task)",
        "sprint_start_date": datetime.date(2021, 3, 29),
        "start_sprint_id": 54,
        "members": ["ivan", "hai", "till", "jinay"],
        "to_do_status": ["Selected for Development"],
    },
    "research": {
        "sprint_query": "project in ('ML') AND status changed to 'Done' after '{start_date}' before '{end_date}' AND issuetype in (Story, Subtask, Bug, Task)",
        "sprint_start_date": datetime.date(2021, 3, 29),
        "start_sprint_id": 54,
        "members": [
            "buddhi",
            "hala",
            "sumit",
            "manuel",
        ],
        "to_do_status": ["To Do"],
    },
}
