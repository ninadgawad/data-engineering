## Documentation:
A python streamlit app to create, update, transition JIRA tickets using API calls from a streamlit application


### Imports and Constants:

- **streamlit as st**: Streamlit library for creating web applications.
- **requests**: HTTP library for making API calls.
- **json**: JSON library for handling JSON data.

## Constants 
- JIRA_URL
- JIRA_USER
- JIRA_API_TOKEN
- JIRA_HEADERS

These are defined for Jira API authentication and requests.

### Streamlit Application:

### Title: The application title is set using st.title.
- Create Jira Ticket Function: create_jira_ticket function to create a new Jira ticket.
- Update Jira Ticket Function: update_jira_ticket function to update an existing Jira ticket.
- Transition Jira Ticket Function: transition_jira_ticket function to transition a Jira ticket's status.


### Streamlit Forms:
- Create Ticket Form: A form for creating a Jira ticket. Users input project key, summary, description, and issue type.
- Update Ticket Form: A form for updating a Jira ticket. Users input ticket ID and optional fields to update (summary, description, issue type).
- Transition Ticket Form: A form for transitioning a Jira ticket. Users input ticket ID and transition ID.
