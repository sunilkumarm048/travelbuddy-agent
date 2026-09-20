import os

from dotenv import load_dotenv
from serpapi import GoogleSearch
from langchain_core.tools import tool

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not SERPAPI_API_KEY:
    raise ValueError("SERPAPI_API_KEY is not configured.")


@tool
def search_flights(
    departure: str,
    arrival: str,
    outbound_date: str,
) -> str:
    """
    Search available one-way flights between two airports
    for a specific departure date.
    """

    params = {
        "engine": "google_flights",
        "departure_id": departure,
        "arrival_id": arrival,
        "outbound_date": outbound_date,
        "type": "2",
        "currency": "INR",
        "hl": "en",
        "api_key": SERPAPI_API_KEY,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "error" in results:
        return f"Flight search error: {results['error']}"

    flights = []

    all_flights = (
        results.get("best_flights", [])
        + results.get("other_flights", [])
    )

    for option in all_flights[:10]:

        segments = option.get("flights", [])

        if not segments:
            continue

        first_segment = segments[0]

        flights.append(
            {
                "airline": first_segment.get("airline"),
                "flight_number": first_segment.get("flight_number"),
                "departure": first_segment.get(
                    "departure_airport", {}
                ).get("time"),
                "arrival": first_segment.get(
                    "arrival_airport", {}
                ).get("time"),
                "duration_minutes": option.get("total_duration"),
                "price_inr": option.get("price"),
                "travel_class": first_segment.get("travel_class"),
            }
        )

    if not flights:
        return "No flights found."

    output = ["Available flights:"]

    for index, flight in enumerate(flights, start=1):

        output.append(
            f"""
Flight {index}
Airline: {flight['airline']}
Flight Number: {flight['flight_number']}
Departure: {flight['departure']}
Arrival: {flight['arrival']}
Duration: {flight['duration_minutes']} minutes
Price: ₹{flight['price_inr']}
Class: {flight['travel_class']}
"""
        )

    return "\n".join(output)


if __name__ == "__main__":

    result = search_flights.invoke(
        {
            "departure": "HYD",
            "arrival": "DEL",
            "outbound_date": "2026-10-15",
        }
    )

    print(result)
    