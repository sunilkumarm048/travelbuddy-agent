import streamlit as st

from app import travel_buddy


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="TravelBuddy",
    page_icon="✈️",
    layout="centered",
)


# ============================================================
# Header
# ============================================================

st.title("✈️ TravelBuddy")
st.subheader("AI-Powered Travel Assistant")

st.write(
    "Plan your trip, research destinations, and find available flights "
    "using AI."
)


# ============================================================
# Travel Inputs
# ============================================================

col1, col2 = st.columns(2)

with col1:
    departure = st.text_input(
        "From",
        placeholder="e.g. Hyderabad",
    )

with col2:
    destination = st.text_input(
        "Destination",
        placeholder="e.g. Delhi",
    )


travel_date = st.date_input(
    "Travel Date"
)


# ============================================================
# Search Button
# ============================================================

search_button = st.button(
    "🔍 Search Travel",
    use_container_width=True,
)


# ============================================================
# Search
# ============================================================

if search_button:

    if not departure or not destination:

        st.warning(
            "Please enter both departure and destination."
        )

    else:

        request = f"""
        I want to plan a trip from {departure} to {destination}
        on {travel_date.strftime('%B %d, %Y')}.

        Research {destination} as a travel destination and find
        available flights from {departure} to {destination}.

        Give me:

        1. Popular attractions
        2. Culture and food
        3. Useful travel tips
        4. Available flight options

        Present the answer in a clear and easy-to-read format.
        """

        # ----------------------------------------------------
        # Show progress
        # ----------------------------------------------------

        with st.spinner(
            "🔎 Researching destination and searching flights..."
        ):

            try:

                response = travel_buddy(request)

                st.success("Travel information found!")

                # ------------------------------------------------
                # Display Gemini response
                # ------------------------------------------------

                if isinstance(response.content, list):

                    for block in response.content:

                        if (
                            isinstance(block, dict)
                            and block.get("type") == "text"
                        ):

                            st.markdown(
                                block.get("text", "")
                            )

                else:

                    st.markdown(response.content)

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )