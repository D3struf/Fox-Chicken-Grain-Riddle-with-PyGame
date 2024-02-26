import unittest
from app import State, breadth_first_search, print_solution

class TestBreadthFirstSearch(unittest.TestCase):
    def test_breadth_first_search_valid_solution(self):
        # Test with a valid initial state
        initial_state = State(0, 1, 0, 1)
        solution = breadth_first_search(initial_state)
        self.assertIsNotNone(solution)
        self.assertTrue(all(isinstance(state, State) for state in solution))
        self.assertTrue(all(state.is_valid() for state in solution))
        self.assertTrue(solution[-1].is_goal_state())

    def test_breadth_first_search_invalid_initial_state(self):
        # Test with an invalid initial state
        initial_state = State(1, 1, 0, 1)  # Invalid initial state
        solution = breadth_first_search(initial_state)

if __name__ == '__main__':
    unittest.main()
