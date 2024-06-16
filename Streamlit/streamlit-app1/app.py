import streamlit as st
import requests
import json

# Jira API details
JIRA_URL = "https://your-jira-instance.atlassian.net"
JIRA_USER = "your-email@example.com"
JIRA_API_TOKEN = "your-api-token"
JIRA_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {JIRA_USER}:{JIRA_API_TOKEN}"
}

# Streamlit application for Jira ticket management
st.title("Jira Ticket Management")

# Function to create a Jira ticket
def create_jira_ticket(project_key, summary, description, issue_type):
    url = f"{JIRA_URL}/rest/api/2/issue"
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        }
    }
    response = requests.post(url, headers=JIRA_HEADERS, data=json.dumps(payload))
    return response.json()

# Function to update a Jira ticket
def update_jira_ticket(ticket_id, fields):
    url = f"{JIRA_URL}/rest/api/2/issue/{ticket_id}"
    payload = {"fields": fields}
    response = requests.put(url, headers=JIRA_HEADERS, data=json.dumps(payload))
    return response.json()

# Function to transition a Jira ticket
def transition_jira_ticket(ticket_id, transition_id):
    url = f"{JIRA_URL}/rest/api/2/issue/{ticket_id}/transitions"
    payload = {"transition": {"id": transition_id}}
    response = requests.post(url, headers=JIRA_HEADERS, data=json.dumps(payload))
    return response.json()

# Streamlit form for creating a Jira ticket
st.subheader("Create a Jira Ticket")
with st.form("create_ticket_form"):
    project_key = st.text_input("Project Key")
    summary = st.text_input("Summary")
    description = st.text_area("Description")
    issue_type = st.text_input("Issue Type")
    create_ticket = st.form_submit_button("Create Ticket")

if create_ticket:
    result = create_jira_ticket(project_key, summary, description, issue_type)
    st.json(result)

# Streamlit form for updating a Jira ticket
st.subheader("Update a Jira Ticket")
with st.form("update_ticket_form"):
    ticket_id = st.text_input("Ticket ID")
    summary = st.text_input("New Summary", "")
    description = st.text_area("New Description", "")
    issue_type = st.text_input("New Issue Type", "")
    update_ticket = st.form_submit_button("Update Ticket")

if update_ticket:
    fields = {}
    if summary:
        fields["summary"] = summary
    if description:
        fields["description"] = description
    if issue_type:
        fields["issuetype"] = {"name": issue_type}
    result = update_jira_ticket(ticket_id, fields)
    st.json(result)

# Streamlit form for transitioning a Jira ticket
st.subheader("Transition a Jira Ticket")
with st.form("transition_ticket_form"):
    ticket_id = st.text_input("Ticket ID")
    transition_id = st.text_input("Transition ID")
    transition_ticket = st.form_submit_button("Transition Ticket")

if transition_ticket:
    result = transition_jira_ticket(ticket_id, transition_id)
    st.json(result)
