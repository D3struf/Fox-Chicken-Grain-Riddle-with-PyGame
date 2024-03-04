# Fox, Chicken and Grain Riddle Problem Agent
# Made by John Paul Monter

from collections import deque

class State:
    def __init__(self, farmer, fox, chicken, grain):
        self.farmer = farmer
        self.fox = fox
        self.chicken = chicken
        self.grain = grain
    
    def is_valid(self):
        return (
            self.is_valid_move(self.fox, self.chicken) and
            self.is_valid_move(self.chicken, self.grain)
        )

    def is_valid_move(self, item1, item2):
        # Check if item1 would eat item2 when left alone
        return not (item1 == item2 and self.farmer != item1)
    
    # Returns the moves or the states
    def possible_moves(self):
        moves = []
        for item in ["farmer", "fox", "chicken", "grain"]:
            if getattr(self, item) == self.farmer:
                new_state = State(
                    1 - self.farmer,
                    self.fox if item != "fox" else 1 - self.fox,
                    self.chicken if item != "chicken" else 1 - self.chicken,
                    self.grain if item != "grain" else 1 - self.grain
                )
                if new_state.is_valid():
                    moves.append(new_state)
        return moves
    
    # Checks to see if all of items are on the other side of the river
    def is_goal_state(self):
        return (
            self.farmer == 1 and
            self.fox == 1 and
            self.chicken == 1 and
            self.grain == 1
        )

    def __str__(self):
        return f"| Farmer: {self.farmer} | Fox: {self.fox} | Chicken: {self.chicken} | Grain: {self.grain} | \n|-----------|--------|------------|----------|"

def breadth_first_search(initial_state):
    if not initial_state.is_valid():
        print("Invalid initial state!")
        return None
    
    visited = set()
    queue = deque([(initial_state, [])])

    while queue:
        state, path = queue.popleft()
        if state.is_goal_state():
            return path + [state]
        if state not in visited:
            visited.add(state)
            for next_state in state.possible_moves():
                queue.append((next_state, path + [state]))

    return None

def print_solution(solution):
    if solution:
        no_valid_states = len(solution)
        print("Number of Valid States:", no_valid_states)
        print("Solution found!")
        print("|-----------|--------|------------|----------|")
        for i, state in enumerate(solution):
            print(f"{state}")
    else:
        print("No solution found.")

# Initial state: Farmer, Fox, Chicken, Grain 
# (0 represents they are on the left side)
# (1 represents they are on the other side)
initial_state = State(0, 1, 0, 0)
print_solution(breadth_first_search(initial_state))
