from contextlib import contextmanager
from tqdm import tqdm
import csv
from typing import Literal, TypedDict
import requests

URL = "https://www.kpedia.jp/p/304-2?nCP={0}"
PAGE_RANGE = range(1, 101 + 1)


def get_page_htmls():
    for page in tqdm(PAGE_RANGE):
        yield requests.get(URL.format(page)).text


def get_words_from_html(html: str):
    table = html.split(r'<table class="school-course">')[1].split(r"</table>")[0]

    for word_html in table.split(r"<tr>")[2:]:
        word = word_html.split(r"</td>")[0].split(r"<td>")[1]
        meaning = word_html.split(r"&nbsp;</a>")[0].split(r'">')[1]

        if word == "" or meaning == "":
            continue

        yield word, meaning


def get_words():
    for html in get_page_htmls():
        for x in get_words_from_html(html):
            yield x


class Row(TypedDict):
    front_text: str
    back_text: str
    comment: str
    front_text_language: Literal["ko-KR"]
    back_text_language: Literal["ja-JP"]


@contextmanager
def open_csv():
    with open("export.csv", "w") as f:
        writer = csv.DictWriter(f, Row.__annotations__.keys())
        yield writer


def run():
    with open_csv() as writer:
        for word, meaning in tqdm(get_words()):
            writer.writerow(
                Row(
                    front_text=word,
                    back_text=meaning,
                    comment="",
                    front_text_language="ko-KR",
                    back_text_language="ja-JP",
                )
            )


if __name__ == "__main__":
    run()
