import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()


def extract_text_from_adf(node: Any) -> str:
    """
    Rekurzivno izdvaja običan tekst iz Jira ADF strukture.

    Jira Cloud description polje može biti vraćeno kao
    Atlassian Document Format (ADF) JSON struktura.
    """

    if node is None:
        return ""

    if isinstance(node, str):
        return node

    if isinstance(node, list):
        parts = [
            extract_text_from_adf(item)
            for item in node
        ]

        return " ".join(
            part.strip()
            for part in parts
            if part.strip()
        )

    if not isinstance(node, dict):
        return str(node)

    node_type = node.get("type", "")

    if node_type == "text":
        return node.get("text", "")

    if node_type == "hardBreak":
        return "\n"

    content = node.get("content", [])

    extracted_parts = [
        extract_text_from_adf(item)
        for item in content
    ]

    separator = "\n" if node_type in {
        "doc",
        "paragraph",
        "heading",
        "listItem",
    } else " "

    text = separator.join(
        part.strip()
        for part in extracted_parts
        if part.strip()
    )

    return text.strip()


def validate_jira_config() -> dict[str, str]:
    """
    Učitava i proverava JIRA konfiguraciju iz .env fajla.
    """

    config = {
        "url": os.getenv("JIRA_URL", "").strip(),
        "email": os.getenv("JIRA_EMAIL", "").strip(),
        "token": os.getenv("JIRA_API_TOKEN", "").strip(),
        "project_key": os.getenv(
            "JIRA_PROJECT_KEY",
            "",
        ).strip(),
    }

    missing_values = [
        key
        for key, value in config.items()
        if not value
    ]

    if missing_values:
        raise RuntimeError(
            "Nedostaju JIRA konfiguracione vrednosti: "
            + ", ".join(missing_values)
        )

    return config


def load_user_stories_from_jira() -> list[dict]:
    """
    Učitava Story issues iz JIRA Cloud projekta
    i pretvara ih u format koji koristi story_analyzer.py.
    """

    config = validate_jira_config()

    jira_url = config["url"].rstrip("/")
    project_key = config["project_key"]

    endpoint = f"{jira_url}/rest/api/3/search/jql"

    jql = (
        f'project = "{project_key}" '
        'AND issuetype = Story '
        'ORDER BY created ASC'
    )

    headers = {
        "Accept": "application/json",
    }

    auth = (
        config["email"],
        config["token"],
    )

    params = {
        "jql": jql,
        "maxResults": 100,
        "fields": (
            "summary,description,"
            "priority,status,issuetype"
        ),
    }

    try:
        response = requests.get(
            endpoint,
            headers=headers,
            auth=auth,
            params=params,
            timeout=30,
        )

    except requests.ConnectionError as error:
        raise RuntimeError(
            "Nije moguće povezivanje sa JIRA serverom."
        ) from error

    except requests.Timeout as error:
        raise RuntimeError(
            "JIRA API zahtev je istekao."
        ) from error

    except requests.RequestException as error:
        raise RuntimeError(
            f"Greška pri JIRA API zahtevu: {error}"
        ) from error

    if response.status_code == 401:
        raise RuntimeError(
            "JIRA autentifikacija nije uspela. "
            "Proveri JIRA_EMAIL i JIRA_API_TOKEN."
        )

    if response.status_code == 403:
        raise RuntimeError(
            "Nemaš dozvolu za pristup traženim JIRA podacima."
        )

    if response.status_code != 200:
        raise RuntimeError(
            "JIRA API greška "
            f"({response.status_code}): "
            f"{response.text[:500]}"
        )

    data = response.json()

    issues = data.get("issues", [])

    stories = []

    for issue in issues:
        fields = issue.get("fields", {})

        priority_data = fields.get("priority") or {}
        status_data = fields.get("status") or {}

        description = extract_text_from_adf(
            fields.get("description")
        )

        story = {
            "id": issue.get("key", ""),
            "title": fields.get("summary", ""),
            "description": description,
            "priority": priority_data.get("name", ""),
            "status": status_data.get("name", ""),
        }

        stories.append(story)

    return stories