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


if sprints:
    st.beta_container()

    st.markdown("## Story points planned/achieved")
    width = 0.25

    x = np.arange(len(sprints))

    fig, ax = plt.subplots(figsize=(15, 8))
    rects1 = ax.barh(x - width, capacity, width, label="Planned")
    rects2 = ax.barh(x, done_sps, width, label="Achieved")
    rects3 = ax.barh(
        x + width, post_estimates, width, label="Post sprint estimates"
    )

    ax.set_xlabel("Story points")
    # ax.set_title("Story points planned/achieved")
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
    # ax.plot(sprints, estimation_acc, label="Estimation Acc")

    # ax.set(
    #     title="Velocity",
    # )
    ax.grid()
    ax.legend()

    st.pyplot(fig)
