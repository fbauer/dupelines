import unittest
from cStringIO import StringIO
import dupelines
from pprint import pformat
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
        expected_lines = \
                        [((0, 0), (0, 15), '["first line",\n'),
                         ((1, 0), (1, 15), '"second line",\n'),
                         ((2, 0), (2, 14), '"third line",\n'),
                         ((3, 0), (3, 13), '"duplicate",\n'),
                         ((4, 0), (4, 13), '"duplicate",\n'),
                         ((5, 0), (5, 13), '"duplicate",\n'),
                         ((6, 0), (6, 6), '"end"]')]
        self.assertEqual(lines, expected_lines, '%s\n!=\n%s' %(pformat(lines), pformat(expected_lines))) 
 
    def test_get_python_tokens(self):
        toks = list(dupelines.get_python_tokens(self.sample_file))
        expected_toks = [((1, 0), (1, 1), '['),
                         ((1, 1), (1, 13), '"first line"'),
                         ((1, 13), (1, 14), ','),
                         ((1, 14), (1, 15), '\n'),
                         ((2, 0), (2, 13), '"second line"'),
                         ((2, 13), (2, 14), ','),
                         ((2, 14), (2, 15), '\n'),
                         ((3, 0), (3, 12), '"third line"'),
                         ((3, 12), (3, 13), ','),
                         ((3, 13), (3, 14), '\n'),
                         ((4, 0), (4, 11), '"duplicate"'),
                         ((4, 11), (4, 12), ','),
                         ((4, 12), (4, 13), '\n'),
                         ((5, 0), (5, 11), '"duplicate"'),
                         ((5, 11), (5, 12), ','),
                         ((5, 12), (5, 13), '\n'),
                         ((6, 0), (6, 11), '"duplicate"'),
                         ((6, 11), (6, 12), ','),
                         ((6, 12), (6, 13), '\n'),
                         ((7, 0), (7, 5), '"end"'),
                         ((7, 5), (7, 6), ']')]
        self.assertEqual(toks, expected_toks)

if __name__ == '__main__':
    unittest.main()


# vim: ts=4 et sw=4
