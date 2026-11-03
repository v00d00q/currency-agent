# Part of the code: what it does
# agent
# system_prompt: the agent's job description
# ask_agent: sends your question to the agent and returns its final answer
# Try it: change the question to "How much is 75 British pounds in Japanese yen?"
# Save the file, and run the Streamlit app.
# Part 5: Add a web page
import os

import streamlit as st

# On the internet, the key comes from Streamlit's Secrets box.
# On your computer, agent.py reads it from the .env file instead.
try:
	if "GOOGLE_API_KEY" in st.secrets:
		os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except st.errors.StreamlitSecretNotFoundError:
	pass

from agent import ask_agent

st.title("💱 My AI Currency Converter")
st.write("Ask a question, and the agent will look up today's exchange rate.")

question = st.text_input(
	"Your question",
	placeholder="Example: How much is 250 US dollars in euros today?",
)

if st.button("Convert"):
	if question.strip():
		with st.spinner("Checking today's rate..."):
			answer = ask_agent(question)
		# A dollar sign can change how Streamlit displays text, so protect it.
		st.success(answer.replace("$", r"\$"))
	else:
		st.warning("Please type a question first.")