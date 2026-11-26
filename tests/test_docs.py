from django.template import Engine


def test_template_engine_exists_for_swagger_page() -> None:
    assert Engine.get_default() is not None
