import datetime
from typing import Dict
import streamlit as st
from jira import JIRA

from log import logger
from constants import (
    STORY_POINTS_FIELD_NAME,
    POST_SPRINT_ESTIMATE_FIELD_NAME,
    SPRINT_LENGTH,
    END_DATE,
    JIRA_SERVER,
    JIRA_USERNAME,
    TEAM_CONSTANTS,
)

options = {"server": JIRA_SERVER}
logger.info("connecting to JIRA")
jira = JIRA(options, basic_auth=(JIRA_USERNAME,st.secrets["jira_token"] ))


def parse_date(s: str):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f%z")


def average(lst):
    return sum(lst) / len(lst)


def get_all_sprints(team):
    sprints = []
    sprint_id = TEAM_CONSTANTS[team]["start_sprint_id"]
    sprint_start_date = TEAM_CONSTANTS[team]["sprint_start_date"]
    sprint_end_date = sprint_start_date + datetime.timedelta(
        days=SPRINT_LENGTH
    )
    while sprint_end_date <= END_DATE:
        sprints.append(
            {
                "id": TEAM_CONSTANTS[team]["sprint_name"].format(
                    sprint_id=sprint_id
                ),
                "start_date": sprint_start_date + datetime.timedelta(-1),
                "end_date": sprint_end_date,
            }
        )
        sprint_id += 1
        sprint_start_date = sprint_end_date
        sprint_end_date = sprint_start_date + datetime.timedelta(
            days=SPRINT_LENGTH
        )
        # if sprint_end_date > END_DATE:
        #     sprint_end_date = END_DATE
    return sprints


def get_time_in_status(team: str, interval=7):
    statuses = TEAM_CONSTANTS[team]["statuses"]
    time_in_statuses_per_interval = {}
    date_intervals = []
    start_date = TEAM_CONSTANTS[team]["start_date"]
    end_date = start_date + datetime.timedelta(days=interval)
    while end_date <= END_DATE:
        date_intervals.append((start_date, end_date))
        start_date = end_date
        end_date = start_date + datetime.timedelta(days=interval)
    for interval in date_intervals:
        time_in_statuses_per_interval[interval[1]] = {s: [] for s in statuses}
        query = TEAM_CONSTANTS[team]["status_change_query"].format(
            start_date=interval[0],
            end_date=interval[1],
        )
        issues = jira.search_issues(
            query,
            maxResults=200,
            expand="changelog",
            fields="summary",
        )
        for i in issues:
            in_status_until = None
            last_status = None
            for history in i.changelog.histories:
                for item in history.items:
                    if (
                        item.field != "status"
                        and item.fromString not in statuses
                        and item.toString not in statuses
                    ):
                        continue
                    if item.fromString in statuses and not last_status:
                        last_status = item.fromString
                        in_status_until = parse_date(history.created)
                    if item.toString == last_status:
                        in_status_from = parse_date(history.created)
                        time_spent = (in_status_until - in_status_from).days
                        if time_spent != 0:
                            time_in_statuses_per_interval[interval[1]][
                                last_status
                            ].append(time_spent)
                        if item.fromString in statuses:
                            last_status = item.fromString
                            in_status_until = parse_date(history.created)

    for interval in date_intervals:
        for status in statuses:
            time_in_statuses_per_interval[interval[1]][status] = (
                average(time_in_statuses_per_interval[interval[1]][status])
                if time_in_statuses_per_interval[interval[1]][status]
                else 0
            )
    return time_in_statuses_per_interval


def get_kpis_from_jira(team: str, capacities: Dict = None):
    sprints = get_all_sprints(team)
    logger.info(f"Sprints : {sprints}")

    sprint_stats = {}
    for sprint in sprints:
        done_sps = 0
        estimated_sps = 0
        est_deviations = 0
        number_of_estimated_issues = 0
        over_estimated = 0
        under_estimated = 0
        query = TEAM_CONSTANTS[team]["sprint_query"].format(
            sprint_id=sprint["id"],
            start_date=sprint["start_date"],
            end_date=sprint["end_date"],
        )
        issues = jira.search_issues(
            query,
            maxResults=200,
            fields=f"{STORY_POINTS_FIELD_NAME},{POST_SPRINT_ESTIMATE_FIELD_NAME}",
        )
        logger.info(f"{len(issues)} issues in Sprint {sprint['id']}")
        for i in issues:
            sp = i.raw["fields"][STORY_POINTS_FIELD_NAME]
            est = i.raw["fields"][POST_SPRINT_ESTIMATE_FIELD_NAME]
            if sp:
                done_sps += sp
                if not est:
                    print(f"No story points estimated for {i.key}, original estimate is {sp}")
                est= est if est else sp
                number_of_estimated_issues += 1
                est_deviations += abs(est - sp)
                if est > sp:
                    under_estimated += est - sp
                elif sp > est:
                    over_estimated += sp - est
                estimated_sps += est
                print(f"======== pre estimated = {sp}, post estimated = {est}, issue = {i.key} =======")
                print(f"======== estimated_sps = {estimated_sps} =======")
                print(f"======== under_estimated = {under_estimated}, over_estimated = {over_estimated} =======")
                
        sprint_stats[sprint["end_date"].strftime("%b %d")] = {
            "Capacity": capacities[sprint["id"]] if capacities else 0,
            "Done SPs": done_sps,
            "Over estimations": over_estimated,
            "Under estimations": under_estimated,
            "Estimated SPs": estimated_sps,
            "Velocity": estimated_sps / capacities[sprint["id"]]
            if capacities
            else estimated_sps,
            "Estimation Accuracy": 1
            - (est_deviations / estimated_sps)
            if estimated_sps
            else 0,
        }
    return sprint_stats
