import unittest
from cStringIO import StringIO
import dupelines
sample_text = ('''\
["first line",
"second line",
"third line",
"duplicate",
"duplicate",
"duplicate",
"end"]''')

class generator_tests(unittest.TestCase):

    def setUp(self):
        self.sample_file = StringIO(sample_text)

    def test_get_line_tokens(self):
        lines = list(dupelines.get_line_tokens(self.sample_file))
        self.assertEqual(lines, [])
 
    def test_get_python_tokens(self):

        lines = list(dupelines.get_python_tokens(self.sample_file))
        self.assertEqual(lines, [])
if __name__ == '__main__':
    unittest.main()


# vim: ts=4 et sw=4
