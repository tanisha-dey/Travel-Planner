import streamlit as st
from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM  # Use Ollama instead of LlamaCpp

# Define PlannerState
class PlannerState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "The messages in the conversation"]
    city: str
    interests: List[str]
    itinerary: str

# Load Llama Model via Ollama
llm = OllamaLLM(model="llama3")  # Ensure Llama3 is installed in Ollama

# Define prompts
spots_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a travel assistant. List the top 10 tourist spots in {city} without any bullets or numbering."),
    ("human", "Give me a list of top tourist spots in {city}. Only provide the names, separated by commas.")
])

itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful travel assistant. Create a day trip itinerary for {city} based on the user's interests: {interests}. Provide a brief, bulleted itinerary."),
    ("human", "Create an itinerary for my day trip.")
])

def get_tourist_spots(city: str):
    response = llm.invoke(spots_prompt.format_messages(city=city))
    return response.split(", ") if response else ["No tourist spots found for this city."]


def input_city(city: str, state: PlannerState) -> PlannerState:
    return {
        **state,
        "city": city,
        "messages": state['messages'] + [HumanMessage(content=city)],
    }

def input_interests(interests: str, state: PlannerState) -> PlannerState:
    return {
        **state,
        "interests": [interest.strip() for interest in interests.split(',')],
        "messages": state['messages'] + [HumanMessage(content=interests)],
    }

def create_itinerary(state: PlannerState) -> str:
    response = llm.invoke(itinerary_prompt.format_messages(city=state['city'], interests=", ".join(state['interests'])))
    
    print("DEBUG: AI Response ->", response)  # Debugging output
    
    state["itinerary"] = response
    state["messages"] += [AIMessage(content=response)]
    return response

# Initialize Streamlit app
st.title("🗺️ Travel Itinerary Planner")
st.write("Enter a city to get suggested tourist spots, then select your interests to generate an itinerary.")

# Maintain state using session_state
if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "city": "",
        "interests": [],
        "itinerary": "",
    }

# User enters city
city = st.text_input("Enter the city for your day trip", value=st.session_state.state["city"])

if city:
    suggested_spots = get_tourist_spots(city)
    st.subheader("Suggested Tourist Spots")
    st.write(", ".join(suggested_spots))
    
    # Show interest input only after city is entered
    interests = st.text_input("Enter your chosen places of interest (comma-separated)", value=", ".join(st.session_state.state["interests"]))
    
    # Generate itinerary on button click
    if st.button("Generate Itinerary"):
        if interests:
            st.session_state.state = input_city(city, st.session_state.state)
            st.session_state.state = input_interests(interests, st.session_state.state)
            itinerary = create_itinerary(st.session_state.state)
            st.session_state.state["itinerary"] = itinerary
        else:
            st.warning("Please enter your places of interest.")

# Display the itinerary
if st.session_state.state["itinerary"]:
    st.subheader("Your Itinerary 📌")
    st.markdown(st.session_state.state["itinerary"])
