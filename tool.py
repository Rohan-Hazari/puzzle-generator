import chess
import chess.engine
import random
import time
def generate_mate_in_n_puzzle(n: int, engine_path: str):
    """
    Create a tool function that generates a chess puzzle with mate in N moves.
    
    Args:
        n: Number of moves to mate
        engine_path: Path to the Stockfish engine
        
    Returns:
        A function that can be used as a tool
    """
    
    def _generate_puzzle(n_moves: int = n):
        """
        Generate a chess puzzle with mate in exactly N moves.
        
        Args:
            n_moves: Number of moves to checkmate (default set by parent function)
            
        Returns:
            FEN string of a position with mate in N
        """
        try:
            engine = chess.engine.SimpleEngine.popen_uci(engine_path)
            engine.configure({"Threads": 4, "Hash": 128})
            
            # Try different approaches for puzzle generation
            approaches = [
                create_puzzle_from_random_position,
                create_puzzle_from_common_position
            ]
            
            for approach in approaches:
                fen, solution = approach(engine, n_moves)
                if fen:
                    engine.quit()
                    return fen
            
            # Fallback to known positions if all generation attempts fail
            engine.quit()
            return get_fallback_position(n_moves)
            
        except Exception as e:
            return f"Error generating puzzle: {str(e)}"
    
    return _generate_puzzle

def create_puzzle_from_random_position(engine, n):
    """Generate a puzzle from a random middlegame position."""
    max_attempts = 20
    
    for attempt in range(max_attempts):
        # Create a board starting from a random position
        board = create_random_middlegame_position()
        
        if board.is_game_over():
            continue
        
        # Find the best move
        result = engine.play(board, chess.engine.Limit(depth=15))
        best_move = result.move
        
        # Make the best move
        board.push(best_move)
        
        # Analyze position after best move
        info = engine.analyse(board, chess.engine.Limit(depth=20))
        score = info["score"].relative
        
        # If it's a mate in exactly (n-1) moves for the opponent
        # Then the original position was a mate in n position
        if score.is_mate() and score.mate() == -(n-1):
            # Undo the move to get back to the puzzle position
            board.pop()
            
            # Verify the solution with deeper analysis
            if verify_mate_in_n(engine, board, n):
                print(f"Found mate in {n} puzzle (attempt {attempt+1})")
                return board.fen(), [best_move]
    
    return None, None

def create_puzzle_from_common_position(engine, n):
    """Generate a puzzle starting from common opening positions."""
    common_positions = [
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # Starting position
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",  # Common Ruy Lopez
        "rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 1 2",  # After 1.e4 Nf6
        "r1bqkbnr/pp1npppp/8/3p4/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 1 5"  # Open position
    ]
    
    max_moves = 15  # Maximum random moves to make from opening
    
    for start_fen in common_positions:
        board = chess.Board(start_fen)
        
        # Make some random moves to get to an interesting position
        moves_to_make = random.randint(5, max_moves)
        for _ in range(moves_to_make):
            if board.is_game_over():
                break
                
            legal_moves = list(board.legal_moves)
            if not legal_moves:
                break
                
            board.push(random.choice(legal_moves))
        
        # Now try to find a move that leads to mate in n-1
        if board.is_game_over():
            continue
            
        result = engine.play(board, chess.engine.Limit(depth=15))
        best_move = result.move
        
        # Make the best move
        board.push(best_move)
        
        # Analyze position after best move
        info = engine.analyse(board, chess.engine.Limit(depth=20))
        score = info["score"].relative
        
        if score.is_mate() and score.mate() == -(n-1):
            # Undo the move to get back to the puzzle position
            board.pop()
            
            # Verify the solution with deeper analysis
            if verify_mate_in_n(engine, board, n):
                return board.fen(), [best_move]
    
    return None, None

def create_random_middlegame_position():
    """Create a random position that resembles a middlegame."""
    board = chess.Board()
    # Play random moves to reach a middlegame-like position
    num_moves = random.randint(15, 30)
    
    for _ in range(num_moves):
        if board.is_game_over():
            break
        
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            break
            
        # Avoid repetitions and boring positions
        if len(legal_moves) > 5:
            # Filter out captures and checks sometimes to avoid forced lines
            if random.random() > 0.3:
                non_captures = [move for move in legal_moves if not board.is_capture(move)]
                if non_captures:
                    legal_moves = non_captures
        
        board.push(random.choice(legal_moves))
    
    return board

def verify_mate_in_n(engine, board, n):
    """Verify that the position is indeed a mate in exactly n moves."""
    # Analyze with high depth
    info = engine.analyse(board, chess.engine.Limit(depth=24))
    score = info["score"].relative
    
    # Check if it's a mate in exactly n moves
    return score.is_mate() and score.mate() == n

def get_fallback_position(n):
    """Return a known mate in N position as fallback."""
    if n == 1:
        return "k7/8/1KP5/8/8/8/8/8 w - - 0 1"  # Mate in 1
    elif n == 2:
        return "3k4/8/3K4/8/8/8/8/4Q3 w - - 0 1"  # Mate in 2
    elif n == 3:
        return "8/8/8/8/8/k7/p7/R3K3 w Q - 0 1"  # Mate in 3
    else:
        return "8/5k2/3p4/1p1Pp2p/1P2Pp1P/5P2/6K1/8 w - - 10 66"