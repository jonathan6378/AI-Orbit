from urllib.parse import urlparse, urlunparse


def normalize_name(name: str | None) -> str:
    """Normalize an entity name."""

    if not name:
        return ""

    return " ".join(name.split()).strip()


def normalize_url(url: str | None) -> str:
    """Create a canonical URL representation."""

    if not url:
        return ""

    url = url.strip()

    if not url:
        return ""

    if url.lower().startswith(("http://", "https://")):
        parsed = urlparse(url)
    else:
        parsed = urlparse("https://" + url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")

    return urlunparse(
        (
            scheme,
            netloc,
            path,
            "",
            parsed.query,
            "",
        )
    )