""""The file which simplifies processing of data """

from urllib.parse import urlparse


def extract_domain_from_url(url: str) -> str:
    """
    Extracts the domain name from a given URL.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc
