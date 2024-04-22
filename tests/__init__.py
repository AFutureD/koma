import unittest
import qa


class TestQA(unittest.TestCase):

    def test_entry(self):
        qa.cli()


if __name__ == '__main__':
    unittest.main()
