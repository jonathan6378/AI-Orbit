from src.processing.normalizer import normalize_url


def test_url_normalization():
    assert (
        normalize_url("HTTPS://Example.COM/test/")
        == "https://example.com/test"
    )
