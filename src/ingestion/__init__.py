# Ingestion layer: pulls raw signals from calendar, transcripts, ADO/Jira, GitHub.
# Each module normalises its source into a list of RawEvent dicts before handing off
# to the observation agent.
