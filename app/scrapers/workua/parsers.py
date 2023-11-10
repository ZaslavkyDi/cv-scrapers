import re
from logging import getLogger

from lxml import etree
from lxml.etree import _Element as Element

from app.common.mixins.parser_mixins import LxmlXpathMixin
from app.common.schemas.candidates_result import CandidatesPageResultSchema, CandidateDetailsSchema
from app.scrapers.workua.config import get_workua_settings

logger = getLogger(__name__)


class WorkUACandidatesHtmlParser(LxmlXpathMixin):

    CANDIDATE_CARD_XPATH = "//*[@id='pjax-resume-list']/div[contains(@class, 'resume-link')]"
    CANDIDATE_CARD_POSITION_XPATH = './/h2/a//text()'
    CANDIDATE_CARD_LINK_XPATH = './/h2/a/@href'
    CANDIDATE_CARD_NAME_XPATH = './/div/b/text()'
    CANDIDATE_CARD_DESIRE_COMPENSATION_XPATH = './/h2/span/span/text()'
    CANDIDATE_CARD_AGE_XPATH = './/div/span[@class = "middot"][1]/following-sibling::span[1]/text()'
    CANDIDATE_CARD_LOCATION_XPATH = './/div/span[@class = "middot"][2]/following-sibling::span[1]/text()'

    CURRENT_PAGE_NUMBER_XPATH = "//*[@id='pjax-resume-list']/nav/ul[1]/li[@class='active']/span/text()"
    LAST_PAGE_NUMBER_XPATH = (
        "//ul[@class='pagination pagination-small visible-xs-block']/li/span[@class='text-default']/text()"
    )

    def parse(self, html_content: str, url: str | None) -> CandidatesPageResultSchema:
        root: Element = etree.fromstring(
            text=html_content,
            parser=etree.HTMLParser(),
            base_url=url
        )
        candidate_cards: list[Element] = root.xpath(self.CANDIDATE_CARD_XPATH)

        candidates: list[CandidateDetailsSchema] = [
            self._parse_candidate_card(card) for card in candidate_cards
        ]
        current_page_number = self._get_clean_text(
            element=root,
            xpath=self.CURRENT_PAGE_NUMBER_XPATH,
        )
        return CandidatesPageResultSchema(
            candidates=candidates,
            page_number=int(current_page_number),
        )

    def parse_last_page_number(self, content: str, url: str | None) -> int:
        root: Element = etree.fromstring(
            text=content,
            parser=etree.HTMLParser(),
            base_url=url
        )
        pages_range: str = self._get_clean_text(
            element=root,
            xpath=self.LAST_PAGE_NUMBER_XPATH,
        )
        numbers = [int(i) for i in pages_range.split() if i.isdigit()]

        if not numbers:
            raise ValueError(f"Can not parse number. There is no digit: [{pages_range}]")

        return numbers[-1]

    def _parse_candidate_card(self, candidate_card: Element) -> CandidateDetailsSchema:
        cv_url: str = self._get_url(
            element=candidate_card,
            xpath=self.CANDIDATE_CARD_LINK_XPATH,
            base=get_workua_settings().host,
        )
        position: str = self._get_text(element=candidate_card, xpath=self.CANDIDATE_CARD_POSITION_XPATH)
        name: str = self._get_text(element=candidate_card, xpath=self.CANDIDATE_CARD_NAME_XPATH)

        desire_compensation: str = self._get_clean_text(
            element=candidate_card,
            xpath=self.CANDIDATE_CARD_DESIRE_COMPENSATION_XPATH
        )
        raw_age: str = self._get_text(
            element=candidate_card,
            xpath=self.CANDIDATE_CARD_AGE_XPATH
        )
        location: str = self._get_text(
            element=candidate_card,
            xpath=self.CANDIDATE_CARD_LOCATION_XPATH
        )

        return CandidateDetailsSchema(
            cv_url=cv_url,
            position=position,
            name=name,
            compensation=desire_compensation,
            age=self._parse_age(raw_age),
            location=location,
        )

    @staticmethod
    def _parse_age(raw_age: str | None) -> int | None:
        if not raw_age:
            return

        age_separator = " "
        raw_age = raw_age.strip()
        raw_age = re.sub("\xa0", " ", raw_age)
        numbers: list[int] = [
            int(i) for i in raw_age.split(age_separator) if i.isdigit()
        ]

        number: int | None
        if len(numbers) == 1:
            number = numbers[0]
        else:
            number = None

        return number
