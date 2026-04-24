import pytest

from api_call import MODEL_CONFIG, _resolve_provider_model


def test_resolve_provider_model_accepts_gpt_5_mini_alias() -> None:
    assert _resolve_provider_model("gpt-5-mini") == "openai/gpt-5-mini"


def test_resolve_provider_model_rejects_provider_model_name() -> None:
    with pytest.raises(ValueError):
        _resolve_provider_model("openai/gpt-5-mini")


def test_openai_gpt_5_mini_pins_openai_provider_without_fallbacks() -> None:
    assert MODEL_CONFIG["openai/gpt-5-mini"]["provider"] == {
        "order": ["OpenAI"],
        "allow_fallbacks": False,
    }
