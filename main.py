import chess
from agents import agent
def main():
    # Get the result from the agent
    response = agent.run("Generate a new chess puzzle FEN for a mate in 2 position.")
    
    # Check if the response is a RunResponse object and extract content
    if hasattr(response, 'content'):
        fen = response.content
    else:
        fen = str(response)
    
    # Clean up the FEN string (remove any quotes or extra text)
    fen = fen.strip().strip("'").strip('"')
    
    print("Generated Puzzle FEN:")
    print(fen)
    
    # Verify the FEN is valid
    try:
        board = chess.Board(fen)
        print("FEN is valid!")
        print(f"Side to move: {'White' if board.turn else 'Black'}")
    except ValueError:
        print("Warning: The generated FEN may not be valid.")

if __name__ == "__main__":
    main()