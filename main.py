import chess
from agents import agent
def main():
    # Get the result from the agent
    response = agent.run("""Generate a new chess puzzle using the tool and provide a complete analysis.
                        Finally, strictly output your analysis as a single JSON object with the structure {
                            title,
                            theme,
                            difficulty,
                            hint,
                            solution,
                            mate_in_n,
                            fen,
                        } 
                        Do not include any other text or markdown—just valid JSON.""")
    
    # Check if the response is a RunResponse object and extract content
    if hasattr(response, 'content'):
        puzzle_analysis = response.content
    else:
        puzzle_analysis = str(response)

    print("\n=== CHESS PUZZLE ANALYSIS ===\n")
    print(puzzle_analysis)

if __name__ == "__main__":
    main()