import unittest
from fixtures import *
from htmldiff.utils import *

class TestUtilMethods(unittest.TestCase):
    def test_is_whitelisted_tag(self):
        self.assertTrue(is_whitelisted_tag(img_tag))
        self.assertFalse(is_whitelisted_tag(div_tag))
        self.assertFalse(is_whitelisted_tag(span_tag))

        settings.WHITELISTED_TAGS.append('span')
        self.assertTrue(is_whitelisted_tag(span_tag))
        settings.WHITELISTED_TAGS.pop()

def main():
    unittest.main()

if __name__ == '__main__':
    main()
