import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage

from tools.tavily_tool import search_destination
from tools.flight_tool import search_flights


# ============================================================
# 1. Load environment variables
# ============================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not configured.")


# ============================================================
# 2. Create Gemini LLM
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GOOGLE_API_KEY,
)


# ============================================================
# 3. Register TravelBuddy tools
# ============================================================

tools = [
    search_destination,
    search_flights,
]


# Create a mapping between tool name and tool
tool_map = {
    tool.name: tool
    for tool in tools
}


# Bind tools to Gemini
llm_with_tools = llm.bind_tools(tools)


# ============================================================
# 4. TravelBuddy Agent
# ============================================================

def travel_buddy(user_request: str):

    # Initial user message
    messages = [
        HumanMessage(content=user_request)
    ]

    # --------------------------------------------------------
    # Ask Gemini which tools are required
    # --------------------------------------------------------

    response = llm_with_tools.invoke(messages)

    # Add Gemini response to conversation
    messages.append(response)

    # --------------------------------------------------------
    # Execute tools requested by Gemini
    # --------------------------------------------------------

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        print()
        print("🔧 Calling tool:", tool_name)
        print("Arguments:", tool_args)

        # Find the requested tool
        selected_tool = tool_map[tool_name]

        # Execute the tool
        tool_result = selected_tool.invoke(tool_args)

        # Add tool result to conversation
        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_id,
            )
        )

    # --------------------------------------------------------
    # Send tool results back to Gemini
    # --------------------------------------------------------

    final_response = llm_with_tools.invoke(messages)

    return final_response


# ============================================================
# 5. Run TravelBuddy
# ============================================================

if __name__ == "__main__":

    request = """
    I want to plan a trip from Hyderabad to Delhi on
    October 15, 2026.

    Research Delhi as a travel destination and find
    available flights from Hyderabad to Delhi.

    Give me useful attractions, travel information,
    and flight options.
    """

    # Run the TravelBuddy agent
    response = travel_buddy(request)

    # --------------------------------------------------------
    # Display final response
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("TRAVELBUDDY")
    print("=" * 70)
    print()

    # Gemini may return content as a list of structured blocks.
    # Extract only the actual text response.

    if isinstance(response.content, list):

        for block in response.content:

            if isinstance(block, dict) and block.get("type") == "text":

                print(block.get("text", ""))

    else:

        print(response.content)