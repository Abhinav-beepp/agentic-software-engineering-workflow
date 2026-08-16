"""Representative generated test plan converted into executable-style pytest examples."""

import pytest


def test_http_url_validation_accepts_https():
    from generated_code import validate_http_url

    assert validate_http_url("https://example.com/path") == "https://example.com/path"


def test_http_url_validation_rejects_non_http():
    from generated_code import validate_http_url

    with pytest.raises(ValueError):
        validate_http_url("ftp://example.com/file")
