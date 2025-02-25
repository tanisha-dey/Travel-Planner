# Travel Itinerary Planner

## Overview
This is an AI-powered travel itinerary planner that suggests top tourist spots and generates a customized itinerary based on user interests.

## Features
- **Suggest Tourist Spots**: Lists the top tourist attractions in a given city.
- **User-Defined Interests**: Allows users to input preferred places of interest.
- **AI-Powered Itinerary Generation**: Uses an AI model to create a personalized day trip plan.
- **Streamlit UI**: Provides a simple and interactive interface.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip

### Dependencies
Install the required dependencies using:
```sh
pip install streamlit langchain_ollama
```

## Usage
1. Run the application:
```sh
streamlit run app.py
```
2. Enter a city name to get suggested tourist spots.
3. Input your places of interest (comma-separated).
4. Click "Generate Itinerary" to receive a personalized travel plan.

## File Structure
- `app.py`: Main application script handling user inputs and AI-based itinerary generation.

## Technologies Used
- **Streamlit**: For the UI and user interaction.
- **Langchain Ollama**: For AI-based text generation.
- **Python**: Core programming language.

## Future Enhancements
- Improve AI responses with more detailed itineraries.
- Add support for multi-day trip planning.
- Integrate real-time travel information.



