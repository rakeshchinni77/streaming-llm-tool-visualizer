from app.services.tokenizer import count_tokens


def test_count_tokens_returns_positive_integer() -> None:
    token_count = count_tokens([{"role": "user", "content": "Hello world"}])

    assert token_count > 0
