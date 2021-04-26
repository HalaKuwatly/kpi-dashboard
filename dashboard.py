import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


from clients.jira_client import get_kpis_from_jira
from clients.notion_client import get_capacity

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


with st.spinner(text="Loading data..."):
    capacities = get_capacity()

    kpis = get_kpis_from_jira("nlu", capacities)
    for s, kpi in kpis.items():
        sprints.append(s)
        capacity.append(kpi["Capacity"])
        done_sps.append(kpi["Done SPs"])
        estimation_acc.append(kpi["Estimation Accuracy"])
        post_estimates.append(kpi["Estimated SPs"])
        velocity.append(kpi["Velocity"])
        over_estimated.append(kpi["Over estimations"])
        under_estimated.append(kpi["Under estimations"])


if sprints:
    st.beta_container()

    st.markdown("## Story points planned/achieved")
    width = 0.25

    x = np.arange(len(sprints))

    fig, ax = plt.subplots(figsize=(15, 8))
    rects1 = ax.barh(x - width, capacity, width, label="Capacity")
    rects2 = ax.barh(x, done_sps, width, label="Planned")
    rects3 = ax.barh(
        x + width, post_estimates, width, label="Actual"
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

    st.markdown("## Velocity")
    fig, ax = plt.subplots()

    ax.plot(sprints, velocity, label="Velocity")
    ax.plot(sprints, estimation_acc, label="Estimation Acc")

    ax.grid()
    ax.legend()


    st.pyplot(fig)

    st.markdown("## Estimation Deviations")
    width = 0.25

    x = np.arange(len(sprints))
    print(over_estimated)
    print(under_estimated)

    fig, ax = plt.subplots(figsize=(15, 8))
    rects1 = ax.barh(x, over_estimated, width, label="Over Estimated")
    rects2 = ax.barh(x + width, under_estimated, width, label="Under Estimated")
    

    ax.set_xlabel("Story points")
    ax.set_yticks(x)
    ax.set_yticklabels(sprints)
    ax.legend()

    ax.bar_label(rects1, padding=6)
    ax.bar_label(rects2, padding=6)
    ax.invert_yaxis()

    fig.tight_layout()
    st.pyplot(fig)
