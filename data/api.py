from datetime import datetime, timedelta

import requests


def get_events():
    url_events = "https://geomapindex.com/api/events"
    response = requests.get(url_events)
    return response.json()


def format_event(event):
    return {
        "title": event["title"],
        "start": event["start"],
        "end": event["end"],
        "className": event.get("className"),
        "extendedProps": {"context": event.get("context", "")},
    }


def get_events_by_category(category):
    url_events = f"https://geomapindex.com/api/events/category/{category}"
    try:
        response = requests.get(url_events, timeout=5)
        response.raise_for_status()
        events_data = response.json()
    except Exception:
        return _fallback_events(category)

    formatted_events = []
    for event in events_data:
        try:
            formatted_events.append(format_event(event))
        except KeyError:
            continue

    return formatted_events or _fallback_events(category)


def _fallback_events(category):
    """Return deterministic demo events when the remote API isn't reachable."""
    category_label = category.title() if isinstance(category, str) else "Dash"
    today = datetime.utcnow().date()

    sample = [
        {
            "title": f"{category_label} Kickoff",
            "start": today.strftime("%Y-%m-%d"),
            "end": today.strftime("%Y-%m-%d"),
            "className": "bg-gradient-success",
            "context": "Intro call for the upcoming milestone.",
        },
        {
            "title": "Architecture Review",
            "start": (today + timedelta(days=2)).strftime("%Y-%m-%dT15:00:00"),
            "end": (today + timedelta(days=2)).strftime("%Y-%m-%dT16:00:00"),
            "className": "bg-gradient-info",
            "context": "Deep dive on infrastructure changes.",
        },
        {
            "title": "Release Window",
            "start": (today + timedelta(days=4)).strftime("%Y-%m-%dT21:00:00"),
            "end": (today + timedelta(days=4)).strftime("%Y-%m-%dT23:00:00"),
            "className": "bg-gradient-warning",
            "context": "Blue/green deployment slot.",
        },
    ]
    return [format_event(event) for event in sample]


if __name__ == "__main__":
    category = "Plotly"  # or any other category
    events = get_events_by_category(category)

    if isinstance(events, list):
        for event in events:
            print(event)
    else:
        print(events)
