# ✈️ TravelBuddy Agent

AI-powered travel assistant using **LangChain, Gemini, Tavily, SerpAPI, and Streamlit**.

## 🚀 Live Demo

👉 [Open TravelBuddy](https://travelbuddy-agent-emnvwxrcw2murwo3oy3x5c.streamlit.app/)

## 📌 Overview

TravelBuddy is an AI-powered travel assistant that helps users plan trips by:

- 🔎 Researching travel destinations
- 🏛️ Finding popular attractions
- 🍛 Providing culture and food information
- 💡 Providing useful travel tips
- ✈️ Searching available flight options
- 🤖 Using Gemini to decide which tools are required

## 🏗️ Architecture

```text
User
  │
  ▼
Streamlit UI
  │
  ▼
Gemini
  │
  ├──────────────┐
  ▼              ▼
Tavily         SerpAPI
  │              │
  ▼              ▼
Destination    Flight
Research       Search
  │              │
  └───────┬──────┘
          ▼
        Gemini
          │
          ▼
    Final Response
