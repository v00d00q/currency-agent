import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
# Load the secret API key from the .env file.
load_dotenv()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
	"""Convert money using today's exchange rate. Use three-letter currency codes,
	such as USD and EUR."""
	from_code = from_currency.strip().upper()
	to_code = to_currency.strip().upper()
	# Step 1: Ask Frankfurter for today's exchange rate.
	reply = requests.get(
		f"https://api.frankfurter.dev/v2/rate/{from_code}/{to_code}",
		timeout=15,
	)
	if reply.status_code != 200:
		return f"I could not find an exchange rate from {from_code} to {to_code}."
	data = reply.json()
	rate = data["rate"]
	# Step 2: Let Python do the math, so the answer is exact.
	converted = amount * rate
	# Step 3: Send the facts back to the AI model.
	return (
		f"{amount:,.2f} {from_code} equals {converted:,.2f} {to_code}. "
		f"Exchange rate: {rate}. Rate date: {data.get('date', 'not listed')}."
	)
# Build the agent: the AI model + its tool + its instructions.
agent = create_agent(
model="google_genai:gemini-3.5-flash-lite",
tools=[convert_currency],
system_prompt=(
	"You are a friendly currency assistant. Always use the convert_currency tool"
	"for conversions. Never guess a rate or do the math yourself. If the amount "
	"or a currency is missing, ask for it. Write money with currency codes, such "
	"as 250.00 USD, and do not use currency symbols. Mention the rate date. "
	"Explain that this is a daily reference rate, and a bank may charge a "
	"different rate."
),
)
def ask_agent(question: str) -> str:
    """Send a question to the agent and return its final answer as text."""
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].text


# This part runs only when you run this file directly.
if __name__ == "__main__":
    print(ask_agent("How much is 250 US dollars in euros today?"))
