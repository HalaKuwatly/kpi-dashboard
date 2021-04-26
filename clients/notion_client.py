from notion.client import NotionClient
import streamlit as st
from requests.exceptions import HTTPError

from constants import (
    NOTION_COLLECTION,
    NOTION_URL_BASE,
    NOTION_VIEW,
)

from log import logger


NOTION_CLIENT = {}


def get_client():

    if "client" not in NOTION_CLIENT:
        try:
            NOTION_CLIENT["client"] = NotionClient(token_v2=st.secrets["notion_token"])
        except HTTPError as error:
            if error.response.status_code == 401:
                NOTION_CLIENT["error"] = "Bad Notion TOKEN_V2."
            else:
                NOTION_CLIENT["error"] = str(error)
            NOTION_CLIENT["client"] = None
    if not NOTION_CLIENT["client"] and "error" in NOTION_CLIENT:
        raise Exception(NOTION_CLIENT["error"])
    elif not NOTION_CLIENT["client"]:
        raise Exception("No client.")
    return NOTION_CLIENT["client"]


def get_capacity():
    get_client()
    wds = [
        "wds_ivan",
        "wds_buddhi",
        "wds_hala",
        "wds_sumit",
        "wds_hai",
        "wds_manuel",
        "wds_till",
        "wds_jinay",
    ]
    sprint_id_prop = "sprint_number"
    state_prop = "status"
    try:
        print(NOTION_URL_BASE.format(NOTION_COLLECTION, NOTION_VIEW))
        cv = get_client().get_collection_view(
            NOTION_URL_BASE.format(NOTION_COLLECTION, NOTION_VIEW)
        )
    except Exception as e:
        logger.error(e)
        if str(e) == "Invalid collection view URL":
            raise Exception("Bad view")
        raise

    capacities = {}
    rows = cv.default_query().execute()

    if not rows:
        raise Exception("No Rows found.")
    for p in wds + [sprint_id_prop, state_prop]:
        if not p in [x["slug"] for x in rows[0].schema]:
            raise Exception(f"No {p} found in the notion view.")

    for row in rows:
        sprint_id = row.get_property(sprint_id_prop)
        state = row.get_property(state_prop)
        if state != "DONE":
            continue
        capacity = 0
        for prop in wds:
            value = row.get_property(prop)
            capacity += int(value) * 2
        capacities["Sprint {sprint_id}".format(sprint_id=sprint_id)] = capacity

    return capacities
