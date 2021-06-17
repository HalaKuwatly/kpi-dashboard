import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


from clients.jira_client import get_kpis_from_jira, get_cycle_time_percentage
from clients.notion_client import get_capacity
from dateutil.relativedelta import relativedelta  # to add days or years
import datetime as dt
from constants import TEAM_CONSTANTS

st.set_page_config(page_title="KPIs", page_icon=":chart:")


sprints = []
capacity = []
done_sps = []
velocity = []
estimation_acc = []
post_estimates = []
times_in_status = []
over_estimated = []
under_estimated = []
correct_estimation = []

option = st.selectbox("Please select the team:", ("NLU", "Apps", "Research"))

team = option.lower()

with st.spinner(text="Loading data..."):
    capacities = get_capacity(team)

    kpis = get_kpis_from_jira(team, capacities)
    for s, kpi in kpis.items():
        sprints.append(s)
        capacity.append(kpi["Capacity"])
        done_sps.append(kpi["Done SPs"])
        estimation_acc.append(kpi["Estimation Error"])
        post_estimates.append(kpi["Estimated SPs"])
        velocity.append(kpi["Velocity"])
        over_estimated.append(kpi["Over estimations"])
        under_estimated.append(kpi["Under estimations"])
        correct_estimation.append(kpi["Correct estimations"])


if sprints:
    st.beta_container()

    st.markdown("## Summary")

    st.markdown(f"**Average Velocity** = {sum(velocity) / len(velocity):9.2f}")
    st.markdown(
        f"**Average # SPs done in a sprint** = {sum(post_estimates) / len(post_estimates):9.2f}"
    )
    st.markdown(
        f"**Average Estimation Error** = {sum(estimation_acc) / len(estimation_acc):9.2f}"
    )
    st.markdown("## Story points planned/achieved")
    width = 0.25

    x = np.arange(len(sprints))

    fig, ax = plt.subplots(figsize=(15, 8))
    rects1 = ax.barh(x - width, capacity, width, label="Capacity")
    rects2 = ax.barh(x, done_sps, width, label="Planned")
    rects3 = ax.barh(x + width, post_estimates, width, label="Actual")

    ax.set_xlabel("Story points")
    ax.set_yticks(x)
    ax.set_yticklabels(sprints)
    ax.legend()

    ax.bar_label(rects1, padding=6)
    ax.bar_label(rects2, padding=6)
    ax.bar_label(rects3, padding=6)
    ax.invert_yaxis()

    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("## Velocity")
    fig, ax = plt.subplots()

    ax.plot(sprints, velocity, label="Velocity")
    ax.plot(sprints, estimation_acc, label="Estimation Error")

    ax.grid()
    ax.legend()

    st.pyplot(fig)

    st.markdown("## Estimation Deviations")
    width = 0.25

    x = np.arange(len(sprints))
    print(over_estimated)
    print(under_estimated)

    fig, ax = plt.subplots(figsize=(15, 8))
    rects1 = ax.barh(x - width, over_estimated, width, label="Over Estimated")
    rects2 = ax.barh(x, under_estimated, width, label="Under Estimated")
    rects3 = ax.barh(
        x + width, correct_estimation, width, label="Correctly Estimated"
    )

    ax.set_xlabel("Story points")
    ax.set_yticks(x)
    ax.set_yticklabels(sprints)
    ax.legend()

    ax.bar_label(rects1, padding=6)
    ax.bar_label(rects2, padding=6)
    ax.bar_label(rects3, padding=6)
    ax.invert_yaxis()

    fig.tight_layout()
    st.pyplot(fig)

with st.spinner(text="Loading data..."):
    cycle_time_percentiles, intervals = get_cycle_time_percentage(team)

    if cycle_time_percentiles:
        st.markdown("## Percentage of issues with cycle time < 5 days")
        fig, ax = plt.subplots()

        ax.plot(intervals, cycle_time_percentiles, label="Percentage")

        ax.grid()
        ax.legend()

        st.pyplot(fig)

    st.markdown(
        f"**Average Percentage of issues with cycle time < 5 days** = {sum(cycle_time_percentiles) / len(cycle_time_percentiles):9.2f}"
    )