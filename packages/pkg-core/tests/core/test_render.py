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
                return "fake result"

        render = TestRenderer()
        result = render.render(None)
        assert result == "fake result"
    
    def test_render_able(self):
        class TestRenderer(BaseRenderer):
            def render(self, renderable: RenderAble):
                return "fake result"

        class TestModel(RenderAble):
            pass

        render = TestRenderer()
        model = TestModel()

        result = render.render(model)
        assert result == "fake result"

    def test_render_able_recursive(self):

        class TestInnerModel(RenderAble):
            text: str = "inner"

        class TestModel(RenderAble):
            inner: TestInnerModel = TestInnerModel()
            list_inner: list[TestInnerModel] = [TestInnerModel(), TestInnerModel()]
            dict_inner: dict[str, TestInnerModel] = {"a": TestInnerModel(), "b": TestInnerModel()}

        class TestRenderer(BaseRenderer):
            def render(self, renderable: RenderAble):
                if isinstance(renderable, TestInnerModel):
                    return "inner result"
                if isinstance(renderable, TestModel):
                    return "outer result"
                return "fake result"

        render = TestRenderer()
        model = TestModel()

        model.render(render)
        
        assert model.represent == "outer result"
        
        assert model.inner.represent == "inner result"
        
        for value in model.list_inner:
            assert value.represent == "inner result"

        for value in model.dict_inner.values():
            assert value.represent == "inner result"
