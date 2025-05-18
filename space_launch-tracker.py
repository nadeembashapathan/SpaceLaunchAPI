import requests
from datetime import datetime

API_URL = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"

def fetch_upcoming_launches(limit=5):
    params = {
        "limit": limit,
        "ordering": "net"  # sort by launch date
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return []

def display_launches(launches):
    if not launches:
        print("No upcoming launches found.")
        return

    print(f"\n🚀 Upcoming Space Launches ({len(launches)}):\n")
    for i, launch in enumerate(launches, 1):
        name = launch["name"]
        net = launch["net"]
        location = launch["pad"]["location"]["name"]
        mission = launch["mission"]["description"] if launch.get("mission") else "No mission description."

        # Convert time to readable format
        try:
            launch_time = datetime.fromisoformat(net.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S UTC')
        except ValueError:
            launch_time = net

        print(f"{i}. {name}")
        print(f"   🕒 Launch Time: {launch_time}")
        print(f"   📍 Location: {location}")
        print(f"   📄 Mission: {mission[:150]}{'...' if len(mission) > 150 else ''}")
        print()

def main():
    print("🚀 Welcome to the Space Launch Tracker")
    num = input("How many upcoming launches do you want to see? (default 5): ").strip()
    try:
        limit = int(num) if num else 5
    except ValueError:
        limit = 5

    launches = fetch_upcoming_launches(limit=limit)
    display_launches(launches)

if __name__ == "__main__":
    main()
