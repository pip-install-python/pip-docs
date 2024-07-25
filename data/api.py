import requests


def get_events():
    url_events = "https://geomapindex.com/api/events"
    response = requests.get(url_events)
    return response.json()


def format_event(event):
    return {
        "title": event['title'],
        "start": event['start'],
        "end": event['end'],
        "className": event['className'],
        "context": event['context']
    }


def get_events_by_category(category):
    url_events = f"https://geomapindex.com/api/events/category/{category}"
    response = requests.get(url_events)
    if response.status_code == 200:
        events_data = response.json()
        formatted_events = [format_event(event) for event in events_data]
        return formatted_events
    else:
        return f"Error: {response.status_code}, {response.text}"


if __name__ == "__main__":
    category = "Plotly"  # or any other category
    events = get_events_by_category(category)

    if isinstance(events, list):
        for event in events:
            print(event)
    else:
        print(events)