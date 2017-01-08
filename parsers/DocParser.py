# coding=utf-8
from __future__ import print_function

import re
import pandas


class PubData(object):
    count = None
    authors = None
    n_authors = None
    publication = None
    journal = None
    issn = None
    isbn = None
    link = None
    AIF = None
    IF = None

    def to_string(self):
        return "count: " + str(self.count) + "\n" \
            "authors: " + self.authors + "\n" \
            "n_authors: " + str(self.n_authors) + "\n" \
            "publication: " + self.publication + "\n" \
            "journal: " + self.journal + "\n" \
            "issn: " + str(self.issn) + "\n" \
            "isbn: " + str(self.isbn) + "\n" \
            "link: " + str(self.link) + "\n" \
            "AIF: " + str(self.AIF) + "\n" \
            "IF: " + str(self.IF)


class CSVParser(object):
    re_issn = r"\bISSN: [0-9]{4}-[0-9]{4}"
    re_isbn = r"\bISBN: [0-9]{13}"
    re_journal = r"//(.*?)[.|:|/]"
    re_authors = r"^(.*?) \."
    re_url = r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?"
    pub_list = list()
    elements = list()

    def __init__(self, file_path):
        self.elements = pandas.read_excel(file_path, header=None)
        self.extract_info()

    def extract_info(self):
        count = 1
        for e in self.elements[0]:
            holder = PubData()
            holder.count = str(count)
            self.__parse_publication(e, holder)
            self.pub_list.append(holder)
            count += 1

    def __parse_publication(self, pub_string, holder):
        holder.publication = pub_string
        try:
            holder.issn = re.search(self.re_issn, pub_string).group()
            holder.issn = re.search(r"[0-9]{4}-[0-9]{4}", holder.issn).group()
        except AttributeError:
            pass
        try:
            holder.isbn = re.search(self.re_isbn, pub_string).group()
            holder.isbn = re.search(r"[0-9]{13}", holder.isbn).group()
        except AttributeError:
            pass
        try:
            holder.journal = re.search(self.re_journal, pub_string).group()
            holder.journal = re.sub(r"[//|.|:]", "", holder.journal).strip()
        except AttributeError:
            pass
        try:
            holder.link = re.search(self.re_url, pub_string).group()
        except AttributeError:
            pass
        try:
            holder.authors = re.search(self.re_authors, pub_string).group()
            holder.authors = re.sub(r" ; ", ";", holder.authors)[:-2]
            holder.n_authors = len(holder.authors.split(";"))
        except AttributeError:
            pass

    def get_pubs(self):
        return self.pub_list
