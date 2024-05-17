import unittest
from unittest import IsolatedAsyncioTestCase


class IntegrateTests(unittest.TestCase):

    def testMarkdown(self):
        from loci.infra.renderers.markdown import MarkDown
        from loci.infra.fetchers.apple import AppleNotesFetcher

        markdown = MarkDown()
        fetcher = AppleNotesFetcher(markdown)
        fetcher.start()

        print(fetcher.notes)