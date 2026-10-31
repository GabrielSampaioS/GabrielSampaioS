import json

import requests

URL = "https://leetcode.com/graphql"

QUERY = """
query userProfileCalendar($username: String!, $year: Int) {
    matchedUser(username: $username) {
        username
        userCalendar(year: $year) {
            submissionCalendar
        }
    }
}
"""


def get_calendar(username: str, year: int | None = None) -> dict[str, int]:
    """Retorna {timestamp_unix: submissoes} do calendário do LeetCode."""
    response = requests.post(
        URL,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://leetcode.com/{username}/",
        },
        json={
            "query": QUERY,
            "variables": {"username": username, "year": year},
        },
        timeout=20,
    )
    response.raise_for_status()

    data = response.json().get("data") or {}
    user = data.get("matchedUser")

    if user is None:
        raise ValueError(f"Usuário '{username}' não encontrado no LeetCode")

    return json.loads(user["userCalendar"]["submissionCalendar"])