import unittest

from alphabet import alphabet

class TestAlphabet(unittest.TestCase):
    
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_init(self):
        filepath = "./test/alphabet.txt"
        count = alphabet(filepath)
        self.assertEqual(count[0], ('a', 0.50))
        self.assertEqual(count[1], ('b', 0.25))
        self.assertEqual(count[2], ('c', 0.20))
        self.assertEqual(count[3], ('d', 0.05))

    def test_nofile(self):
        filepath = "./wrong.txt"
        with self.assertRaises(FileNotFoundError):
            count = alphabet(filepath)

    def test_noalphabet(self):
        filepath = "./test/number.txt"
        count = alphabet(filepath)
        self.assertEqual(len(count), 0)

if __name__ == "__main__":
    unittest.main()
