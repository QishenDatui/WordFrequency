import unittest
from verbsphrase import fileWordCounter, alphabet, filePharseCounter, fileVerbsWordCounter, fileVerbsPharseCounter

class TestVerbsPhrase(unittest.TestCase):
    
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

    def test_pharse_init(self):
        filepath = "./test/phrase.txt"
        stopWordpath = None
        phrase = 2
        count = filePharseCounter(filepath, 10, stopWordpath, phrase)
        result = [('hello world', 100), ('hello kit', 30), ('a a', 10), ('a key', 5)]
        self.assertEqual(count, result)

    def test_pharse_stop(self):
        filepath = "./test/phrase.txt"
        stopWordpath = "./stopword.txt"
        phrase = 2
        count = filePharseCounter(filepath, 10, stopWordpath, phrase)
        result = [('hello world', 100), ('a a', 10), ('a key', 5)]
        self.assertEqual(count, result)

    def test_verbsword_init(self):
        filepath = "./test/verbsword.txt"
        stopwordpath = None
        verbs = "./verbs.txt"
        count = fileVerbsWordCounter(filepath, 10, stopwordpath, verbs)
        result = [('abase', 400), ('abate',400), ('the',50)]
        self.assertEqual(count, result)

    def test_verbsword_stop(self):
        filepath = "./test/verbsword.txt"
        stopwordpath = "./stopword.txt"
        verbs = "./verbs.txt"
        count = fileVerbsWordCounter(filepath, 10, stopwordpath, verbs)
        result = [('abase', 400), ('abate',400)]
        self.assertEqual(count, result)

    def test_verbsphrase_init(self):
        filepath = "./test/verbsphrase.txt"
        stopwordpath = None
        verbs = "./verbs.txt"
        phrase = 2
        count = fileVerbsPharseCounter(filepath, 10, stopwordpath, phrase, verbs)
        result = [('abase kit', 100), ('abate boy',100), ('of the',50)]
        self.assertEqual(count, result)

    def test_verbsphrase_stop(self):
        filepath = "./test/verbsphrase.txt"
        stopwordpath = "./stopword.txt"
        verbs = "./verbs.txt"
        phrase = 2
        count = fileVerbsPharseCounter(filepath, 10, stopwordpath, phrase, verbs)
        result = []
        self.assertEqual(count, result)

    def test_verbsphrase_nofile(self):
        filepath = "./wrong.txt"
        verbs = "./verbs.txt"
        with self.assertRaises(FileNotFoundError):
            count = fileVerbsPharseCounter(filepath, 10, None, 2, verbs)


if __name__ == "__main__":
    unittest.main()