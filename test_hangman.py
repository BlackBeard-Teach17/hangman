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

    @patch('builtins.input', return_value='a')
    def test_get_player_input(self, mock_input):
        self.assertEqual(self.game.get_player_input(), 'a')

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

    def test_provide_hint(self):
        self.game.target_word = 'apple'
        self.assertEqual(self.game.provide_hint(self.game.target_word, 'length'), 'The word is: 5 characters.')
        self.assertEqual(self.game.provide_hint(self.game.target_word, 'first_letter'), 'The first letter of the word is: a')
        self.assertEqual(self.game.provide_hint(self.game.target_word, 'last_letter'), 'The last letter of the word is: e')

if __name__ == '__main__':
    unittest.main()