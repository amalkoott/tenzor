import requests
from datetime import datetime, timezone, timedelta


def fetch_json(url):
    response = requests.get(url)
    return response.json()


def print_time(timestamp_ms, timezone_s):
    timestamp_s = timestamp_ms / 1000

    hours = timezone_s // 3600000
    minutes = (timezone_s % 3600000) // 60000

    local_time = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
    local_time_str = local_time.astimezone(timezone(timedelta(hours=hours))).strftime('%Y-%m-%d %H:%M:%S')
    timezone_name = f"UTC{'+' if hours >= 0 else ''}{hours}:{abs(minutes):02d}"

    print(local_time_str, timezone_name)


def average_delta(url):
    deltas = []
    for _ in range(5):
        start_time = datetime.now()
        timestamp_s = fetch_json(url=url)['time'] / 1000
        delta = (datetime.fromtimestamp(timestamp_s) - start_time).total_seconds()
        deltas.append(delta)

    return sum(deltas) / len(deltas)


def main():
    url = "https://yandex.com/time/sync.json?geo=213"

    data = fetch_json(url=url)
    print(data)
    print_time(timestamp_ms=data['time'],timezone_s=data['clocks']['213']['offset'] )

    print(f"average delta = {average_delta(url=url)} s")

if __name__ == "__main__":
    main()