import unittest
from unittest.mock import patch
from hangman import Hangman

class TestHangman(unittest.TestCase):
    def setUp(self):
        self.game = Hangman()

    def test_init(self):
        self.assertEqual(self.game.wrong_guesses, 0)
        self.assertEqual(len(self.game.guessed_letters), 0)
        self.assertEqual(len(self.game.correct_word_list), len(self.game.target_word))

    def test_validate_input(self):
        self.assertTrue(self.game.validate_input('a'))
        self.assertFalse(self.game.validate_input('A'))
        self.assertFalse(self.game.validate_input('1'))
        self.assertFalse(self.game.validate_input('ab'))

    @patch('builtins.input', side_effect=['hint', 'a'])
    @patch('builtins.print')
    def test_get_player_input_hint_no_hints_remaining(self, mock_print, mock_input):
        self.game.hints_remaining = 0
        self.assertEqual(self.game.get_player_input(), 'a')
        mock_print.assert_called_with("You have no hints remaining.")

    @patch('builtins.input', side_effect=['hint', 'a'])
    @patch('builtins.print')
    def test_get_player_input_hint_with_hints_remaining(self, mock_print, mock_input):
        self.game.hints_remaining = 1
        self.game.target_word = 'apple'
        self.assertEqual(self.game.get_player_input(), 'a')
        mock_print.assert_called_with("Hint: The letter 'e' is in the word.")

    @patch('builtins.input', side_effect=['1', 'a'])
    @patch('builtins.print')
    def test_get_player_input_invalid_input(self, mock_print, mock_input):
        self.assertEqual(self.game.get_player_input(), 'a')
        mock_print.assert_called_with("Invalid input. Please enter a single lowercase letter that you haven't guessed before, or type 'hint' for a hint.")
    
    def test_game_over(self):
        self.game.wrong_guesses = self.game.MAX_INCORRECT_GUESSES
        self.assertTrue(self.game.game_over())
        self.game.wrong_guesses = 0
        self.game.guessed_letters = set(self.game.target_word)
        self.assertTrue(self.game.game_over())

    def test_find_letter(self):
        self.game.target_word = 'apple'
        self.assertEqual(self.game.find_letter('a', self.game.target_word), [0])
        self.assertEqual(self.game.find_letter('p', self.game.target_word), [1, 2])

    def test_build_word(self):
        self.game.target_word = 'apple'
        self.game.correct_word_list = ['_', '_', '_', '_', '_']
        self.assertEqual(self.game.build_word('a'), 'a____')
        self.assertEqual(self.game.build_word('p'), 'app__')

    @patch('builtins.print')
    @patch('random.choice', return_value='a')
    def test_get_hint_no_hints_remaining(self, mock_choice, mock_print):
        self.game.hints_remaining = 0
        self.game.get_hint()
        mock_print.assert_called_once_with("You have no hints remaining.")

    @patch('builtins.print')
    @patch('random.choice', return_value='a')
    def test_get_hint_with_hints_remaining(self, mock_choice, mock_print):
        self.game.target_word = 'apple'
        self.game.hints_remaining = 1
        self.game.get_hint()
        mock_print.assert_called_once_with("Hint: The letter 'a' is in the word.")
        self.assertEqual(self.game.hints_remaining, 0)
        

if __name__ == '__main__':
    unittest.main()