import random
import numpy as np
from helper import *

class AIPlayer:

    def __init__(self, player_number: int, timer):
        """
        Intitialize the AIPlayer Agent

        # Parameters
        `player_number (int)`: Current player number, num==1 starts the game
        `timer: Timer`: A Timer object that can be used to fetch the remaining time for any player.
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}: ai'.format(player_number)
        self.timer = timer
        self.moves_count = 0
        self.first_move_corner = None  # Store the initial corner move

    def strategy(self, state):
        """
        Implements your strategy:
        - First move in a corner
        - Next moves in adjacent corners, then focus on edge moves
        - Try to form a bridge or fork

        # Parameters
        `state (np.array)`: The current game board state

        # Returns
        Tuple[int, int]: The selected move coordinates
        """
        
        dim = state.shape[0]
        valid_moves = get_valid_actions(state)
        
        def get_adjacent_corners(corner_index, dim):
            adjacent_corners_list={0:[1,5],1:[0,2],2:[1,3],3:[2,4],4:[3,5],5:[4,0]}
            adjacent_corners=[]
            for next_corner in adjacent_corners_list[corner_index]:                
                adjacent_corners.append(get_vetex_at_corner(next_corner,dim))
            return adjacent_corners
                    
        
        # If board dimension is less than 7, follow the strategy
        if dim < 7:
            corners = get_all_corners(dim)
            
            # First move: place at a random corner
            if self.moves_count == 0:
                # valid_moves=get_valid_actions(state)
                first_move=list(set(corners).intersection(valid_moves))
                self.first_move_corner = random.choice(first_move)
                self.moves_count += 1
                return self.first_move_corner

            # For subsequent moves: place at an adjacent corner
            if self.first_move_corner:
                move= self.first_move_corner
                corner_index = get_corner(move, dim)              
                adjacent_corners = get_adjacent_corners(corner_index, dim)
                valid_adjacent = [move for move in adjacent_corners if move in valid_moves]
                
                if valid_adjacent:
                    return random.choice(valid_adjacent)
            
        # Fallback: Random valid move if no adjacent move found
        return random.choice(valid_moves)

    def get_move(self, state: np.array) -> Tuple[int, int]:
        """
        Given the current state of the board, return the next move based on strategy.

        # Parameters
        `state: np.array`: A numpy array representing the board state.

        # Returns
        Tuple[int, int]: The selected move (coordinates)
        """
        move = self.strategy(state)
        return move
