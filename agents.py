from agno.agent import Agent
from agno.models.google import Gemini
from tool import generate_mate_in_n_puzzle
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_KEY")
# Adjust path to your local stockfish
ENGINE_PATH = "stockfish/stockfish.exe"

agent = Agent(
    model=Gemini(id="gemini-2.0-flash",api_key=api_key),
    tools=[generate_mate_in_n_puzzle(3,ENGINE_PATH)],
    instructions=[
        "When asked for a chess puzzle, call the chess-puzzle-generator tool and return only the FEN string.Do not modify it and validate it"
    ]
)
