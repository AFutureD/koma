import unittest

from loci.infra.renderers import MarkDown
from loci.infra.fetchers.apple import AppleNotesFetcher


class TestQA(unittest.TestCase):

    def test_entry(self):
        markdown = MarkDown()
        AppleNotesFetcher(markdown).start()



