from dotenv import load_dotenv
import os
import google.generativeai as genai
from agents import Agent, Runner, set_tracing_disabled
from agents.models.base import Model

load_dotenv()
set_tracing_disabled(True)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Custom Gemini model wrapper
class GeminiModel(Model):
    def __init__(self, model_name="gemini-pro"):
        self.model = genai.GenerativeModel(model_name)

    async def call(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

# Instantiate the custom model
model = GeminiModel("gemini-pro")

# Web Developer agent
web_developer = Agent(
    name="Web Developer",
    instructions="A web developer who can build websites and web applications",
    model=model,
    handoff_description="handoff to web developer if the task is related to web development"
)

# App Developer agent
app_developer = Agent(
    name="App Developer",
    instructions="Develop cross-platform mobile apps for iOS and Android",
    model=model,
    handoff_description="handoff to mobile app developer if the task is related to app development"
)

# Marketing Agent
marketing = Agent(
    name="Marketing Agent",
    instructions="Create and execute marketing strategies for product launches",
    model=model,
    handoff_description="handoff to marketing agent if the task is related to marketing"
)

# Main manager agent
async def myAgent(user_input):
    manager = Agent(
        name="Manager",
        instructions="""
        You are a helpful assistant that can only help with:
        1. Web Development - Building websites and web applications
        2. Mobile App Development - Creating cross-platform mobile apps for iOS and Android
        3. Marketing - Creating and executing marketing strategies for product launches

        If the user asks for anything else, respond with:
        "Sorry, I can't help about this topic."
        """,
        model=model,
        handoff_description=["web developer", "app developer", "marketing agent"]
    )

    response = await Runner.run(manager, input=user_input)
    return response.final_output
