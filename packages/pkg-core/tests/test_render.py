import pytest
import unittest
from koma.core import TextRenderer, RenderAble


class RenderTests(unittest.TestCase):

    def test_base_render_not_implement(self):
        with pytest.raises(TypeError):
            _ = TextRenderer()

    def test_base_render_implement(self):
        class TestRenderer(TextRenderer):
            def render(self, renderable: RenderAble):
                return "fake result"

        render = TestRenderer()
        result = render.render(None)
        assert result == "fake result"
    
    def test_render_able(self):
        class TestRenderer(TextRenderer):
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

        class TestRenderer(TextRenderer):
            def render(self, renderable: RenderAble):
                if isinstance(renderable, TestInnerModel):
                    return "inner result"
                if isinstance(renderable, TestModel):
                    return "outer result"
                return "fake result"

        render = TestRenderer()
        model = TestModel()

        model.render(render)
        
        assert model.rendered_result == "outer result"
        
        assert model.inner.rendered_result == "inner result"
        
        for value in model.list_inner:
            assert value.rendered_result == "inner result"

        for value in model.dict_inner.values():
            assert value.rendered_result == "inner result"
