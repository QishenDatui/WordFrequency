import unittest
from stopWord import fileWordCounter, alphabet

class TestStopWord(unittest.TestCase):
    
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_alphabet_init(self):
        filepath = "./test/alphabet.txt"
        count = alphabet(filepath)
        self.assertEqual(count[0], ('a', 0.50))
        self.assertEqual(count[1], ('b', 0.25))
        self.assertEqual(count[2], ('c', 0.20))
        self.assertEqual(count[3], ('d', 0.05))

    def test_alphabet_nofile(self):
        filepath = "./wrong.txt"
        with self.assertRaises(FileNotFoundError):
            count = alphabet(filepath)

    def test_alphabet_noalphabet(self):
        filepath = "./test/number.txt"
        count = alphabet(filepath)
        self.assertEqual(len(count), 0)

    def test_word_init(self):
        filepath = "./test/word.txt"
        count = fileWordCounter(filepath, 10, None)
        result = [('word', 100), ('hello', 70), ('a', 60), ('boy', 60), ('key', 50)]
        self.assertEqual(count, result)

    def test_word_noword(self):
        filepath = "./test/noword.txt"
        count = fileWordCounter(filepath, -1, None)
        self.assertEqual(len(count), 0)

    def test_stopWord_init(self):
        filepath = "./test/word.txt"
        stopWordpath = "./stopword.txt"
        count = fileWordCounter(filepath, 10, stopWordpath)
        result = [('word', 100), ('hello', 70), ('a', 60), ('key', 50)]
        self.assertEqual(count, result)

if __name__ == "__main__":
    unittest.main()


