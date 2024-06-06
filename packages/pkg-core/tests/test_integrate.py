import unittest


class IntegrateTests(unittest.TestCase):

    def test_markdown(self):
        from koma.infra.renderers.markdown import MarkDown
        from koma.infra.fetchers.apple import AppleNotesFetcher

        markdown = MarkDown()
        fetcher = AppleNotesFetcher(markdown)
        fetcher.start()