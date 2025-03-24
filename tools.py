from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool("DuckDuckGoSearch")
def duckduckgo_search(query: str) -> str:
    """Search the web using DuckDuckGo."""
    search = DuckDuckGoSearchRun()
    return search.run(query)

@tool("BudgetCalculator")
def budget_calculator(budget: float, duration: int) -> str:
    """Calculate daily spending limits based on total budget and trip duration in INR."""
    if duration <= 0:
        return "Error: Trip duration must be positive."
    daily_budget = budget / duration
    travel_percentage = 0.3
    accommodation_percentage = 0.4
    activities_percentage = 0.3
    return f"Suggested daily spending (in INR):\n" \
           f"- Travel: ₹{daily_budget * travel_percentage:.2f}\n" \
           f"- Accommodation: ₹{daily_budget * accommodation_percentage:.2f}\n" \
           f"- Activities: ₹{daily_budget * activities_percentage:.2f}"