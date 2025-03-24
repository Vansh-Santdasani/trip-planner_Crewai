import yaml
from crewai import Agent, Task, Crew, Process
from langchain_ollama import ChatOllama
from tools import duckduckgo_search, budget_calculator
import requests

# Check if Ollama is running
def check_ollama():
    try:
        response = requests.get("http://localhost:11434")
        if response.status_code == 200:
            print("Ollama server is running.")
        else:
            print("Ollama server is reachable but returned an unexpected status.")
    except requests.ConnectionError:
        print("Error: Ollama server is not running. Please start it with 'ollama run llama3'.")
        exit(1)

# Load YAML configurations
with open('config/agents.yaml', 'r') as f:
    agents_config = yaml.safe_load(f)
with open('config/tasks.yaml', 'r') as f:
    tasks_config = yaml.safe_load(f)

# Verify Ollama before proceeding
check_ollama()

# Set up Ollama LLM with explicit provider prefix
ollama_llm = ChatOllama(
    model="ollama/llama3.2:3b",  # Prefix with 'ollama/' to specify the provider
    base_url="http://localhost:11434"  # Default Ollama URL
)

# Define tools dictionary
tools = {
    "DuckDuckGoSearch": duckduckgo_search,
    "BudgetCalculator": budget_calculator
}

# Get user input
print("Welcome to the Travel Planning Assistant!")
preference = input("What city are you interested in ?  ")
budget = float(input("What is your total budget for the trip? (in Rupees): "))
duration = int(input("How many days do you plan to travel?: "))

# Create agents
research_agent = Agent(
    role=agents_config['research_agent']['role'],
    goal=agents_config['research_agent']['goal'],
    backstory=agents_config['research_agent']['backstory'],
    llm=ollama_llm,
    tools=[tools[tool] for tool in agents_config['research_agent']['tools']],
    verbose=True
)

budget_agent = Agent(
    role=agents_config['budget_agent']['role'],
    goal=agents_config['budget_agent']['goal'],
    backstory=agents_config['budget_agent']['backstory'],
    llm=ollama_llm,
    tools=[tools[tool] for tool in agents_config['budget_agent']['tools']],
    verbose=True
)

itinerary_agent = Agent(
    role=agents_config['itinerary_agent']['role'],
    goal=agents_config['itinerary_agent']['goal'],
    backstory=agents_config['itinerary_agent']['backstory'],
    llm=ollama_llm,
    tools=[tools[tool] for tool in agents_config['itinerary_agent']['tools']],
    verbose=True
)

# Create tasks with formatted descriptions
research_destinations = Task(
    description=tasks_config['research_destinations']['description'].format(preference=preference),
    expected_output=tasks_config['research_destinations']['expected_output'],
    agent=research_agent
)

analyze_budget = Task(
    description=tasks_config['analyze_budget']['description'].format(budget=budget, duration=duration),
    expected_output=tasks_config['analyze_budget']['expected_output'],
    agent=budget_agent
)

create_itinerary = Task(
    description=tasks_config['create_itinerary']['description'].format(duration=duration),
    expected_output=tasks_config['create_itinerary']['expected_output'],
    agent=itinerary_agent
)

# Create crew with sequential process
crew = Crew(
    agents=[research_agent, budget_agent, itinerary_agent],
    tasks=[research_destinations, analyze_budget, create_itinerary],
    process=Process.sequential,
    verbose=True
)

# Run the crew and display results
print("\nGenerating your personalized travel plan...")
result = crew.kickoff()
print("\n=== Your Travel Itinerary ===")
print(result)