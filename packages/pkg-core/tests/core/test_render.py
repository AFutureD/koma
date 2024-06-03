import pytest
import unittest
from unittest.mock import patch
from loci.core import BaseRenderer, RenderAble


class RenderTests(unittest.TestCase):

    def test_base_render_not_implement(self):
        with pytest.raises(TypeError):
            _ = BaseRenderer()

    def test_base_render_implement(self):
        class TestRenderer(BaseRenderer):
            def render(self, renderable: RenderAble):
                pass

        with patch.object(TestRenderer, 'render', return_value=None) as mock_method:
            render = TestRenderer()
            render.render(RenderAble())
        mock_method.assert_called_once()

