import re
from urllib.parse import urljoin

from lxml.etree import _Element as Element


class LxmlXpathMixin:

    def _get_text(self, element: Element, xpath: str) -> str:
        if not xpath.endswith("/text()"):
            raise ValueError(f"To use this function the given XPATH has to end on '/text()'")

        results: list[str] = element.xpath(xpath)
        return " ".join(results)

    def _get_url(self, element: Element, xpath: str, base: str = "") -> str:
        if not xpath.endswith("@href"):
            raise ValueError(f"To use this function the given XPATH has to end on '@href'")

        results: list[str] = element.xpath(xpath)
        if not results:
            raise ValueError("Can not find urls attribute.")

        return urljoin(base=str(base), url=results[0])

    def _get_clean_text(self, element: Element, xpath: str) -> str:
        text: str = self._get_text(element, xpath)

        text = text.strip()
        text = re.sub(r"\t", "", text)
        text = re.sub(r"\n", " ", text)

        return text
