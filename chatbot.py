from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools import tool
from datetime import datetime
import requests

# 🕒 Tool 1: Get current time
@tool
def get_time() -> str:
    """Return the current local date and time."""
    return datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")

# 🌦️ Tool 2: Get weather by city name
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city using the wttr.in API."""
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Couldn't fetch weather for {city} (status {response.status_code})."
    except Exception as e:
        return f"Error fetching weather: {e}"

# 🧠 Connect to your local Ollama model (✅ use `id=` in Agno v2.1.9)
local_llm = Ollama(id="mistral")

# 🤖 Define the chatbot agent
chatbot = Agent(
    name="LocalChatbot",
    model=local_llm,
    instructions="You are a helpful local chatbot. Use tools to get the current time or weather when needed.",
    tools=[get_time, get_weather],
)

print("🤖 Local chatbot is running. Type 'exit' to quit.\n")

# 💬 Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    chatbot.print_response(user_input, stream=True)
    print()
