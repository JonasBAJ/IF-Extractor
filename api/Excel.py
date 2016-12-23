# coding=utf-8
from __future__ import print_function

import re

from xlsxwriter import Workbook
from xlsxwriter.utility import xl_cell_to_rowcol, xl_rowcol_to_cell

from vu.Structures import HEADER_STYLE, PUB_STYLE


class ExcelWriter(Workbook):
    header_style = None
    pub_style = None
    ws = None

    def __init__(self, filename):
        super(ExcelWriter, self).__init__(filename, {})
        self.ws = self.add_worksheet()
        self.header_style = self.add_format(HEADER_STYLE)
        self.pub_style = self.add_format(PUB_STYLE)

    def print_header(self):
        self.ws.write("B1", None, self.header_style)
        self.ws.write("C1", "Visų autorių skaičius (NA)".decode("utf8"), self.header_style)
        self.ws.write("D1", "Instituc. (padalinio) autorių skaičius (NIA)".decode("utf8"), self.header_style)
        self.ws.write("E1", "Instituc. (padalinio) autorių indėlis".decode("utf8"), self.header_style)
        self.ws.write("F1", "Prieskyrų (afiliacijų) skaičius (NIP)".decode("utf8"), self.header_style)
        self.ws.write("G1", "Mokslo sritis".decode("utf8"), self.header_style)
        self.ws.write("H1", "Publikacijos tipas".decode("utf8"), self.header_style)
        self.ws.write("I1", "Žurnalo cit. rodiklis (impact factor) IF".decode("utf8"), self.header_style)
        self.ws.write("J1", "Agreg. cit. rodiklis (agregate impact factor) AIF".decode("utf8"), self.header_style)
        self.ws.write("K1", "I kriterijus [IF/(AIF*0.2)]".decode("utf8"), self.header_style)
        self.ws.write("L1", "CHF balas".decode("utf8"), self.header_style)

    def print_publications(self, pubs):
        self.print_header()
        i = 0
        for p in pubs:
            self.print_static(i)
            self.ws.write(self.inc("A3", i, 0), p.count, None)
            # Publications
            self.ws.merge_range(self.inc("C3:L3", i, 0), p.publication, self.pub_style)
            self.ws.merge_range(self.inc("C4:L4", i, 0), p.authors, self.pub_style)
            # self.ws.merge_range(self.inc("C5:L5", i, 0), None, self.pub_style)
            self.ws.write(self.inc("C6", i, 0), p.n_authors, self.pub_style)
            self.ws.write(self.inc("I6", i, 0), p.IF, self.pub_style)
            self.ws.write(self.inc("J6", i, 0), p.AIF, self.pub_style)
            self.ws.merge_range(self.inc("C7:L7", i, 0), p.issn, self.pub_style)
            self.ws.merge_range(self.inc("C8:L8", i, 0), p.isbn, self.pub_style)
            self.ws.merge_range(self.inc("C9:L9", i, 0), p.journal, self.pub_style)
            self.ws.merge_range(self.inc("C10:L10", i, 0), p.link, self.pub_style)
            self.ws.merge_range(self.inc("C11:L11", i, 0), None, self.pub_style)
            # Formulas
            self.print_formulas(i)
            i += 10

    def print_formulas(self, i):
        i6 = self.inc("I6", i, 0)
        j6 = self.inc("J6", i, 0)
        d6 = self.inc("D6", i, 0)
        f6 = self.inc("F6", i, 0)
        c6 = self.inc("C6", i, 0)
        e6 = self.inc("E6", i, 0)
        l6 = self.inc("L6", i, 0)
        k6 = self.inc("K6", i, 0)
        c5_l5 = self.inc("C5:L5", i, 0)
        if_aif_ratio = "=IF(OR(" + i6 + "=0," + j6 + "=0), \"\", " + i6 + "/(" + j6 + "*0.2))"
        chf_value = "=IF(OR(" + i6 + "=\"\"," + j6 + "=\"\", " + c6 + "=\"\", " + d6 + "=\"\"), \"\", " \
                    "3*(" + d6 + "*SQRT(1+" + f6 + ")/" + c6 + ")*(2*" + i6 + "/" + j6 + "+1))"
        author_ratio = "=IF(OR(" + c6 + "=\"\", " + d6 + "=\"\"), \"\", " + d6 + "/" + c6 + ")"
        chf_author_count = "=IF(COUNTA(" + c5_l5 + ")=0, \"\", COUNTA(" + c5_l5 + "))"
        self.ws.write(k6, if_aif_ratio, self.pub_style)
        self.ws.write(l6, chf_value, self.pub_style)
        self.ws.write(e6, author_ratio, self.pub_style)
        self.ws.write(d6, chf_author_count, self.pub_style)
        for n in range(9):
            n3 = self.inc("N3", i+n, 0)
            o3 = self.inc("O3", i+n, 0)
            c5 = self.inc("C5", i, n)
            author = "=IF(NOT(" + c5 + "=0), " + c5 + ", \"\")"
            author_score = "=IF(" + n3 + "=\"\", \"\", " + l6 + "/" + d6 + ")"
            self.ws.write(n3, author, self.pub_style)
            self.ws.write(o3, author_score, self.pub_style)

    def print_static(self, i):
        self.ws.write(self.inc("B3", i, 0), "Visas bibliografinis aprašas".decode("utf8"), self.header_style)
        self.ws.write(self.inc("B4", i, 0), "Visi Autoriai".decode("utf8"), self.header_style)
        self.ws.write(self.inc("B5", i, 0), "Institucijos autoriai".decode("utf8"), self.header_style)
        self.ws.write(self.inc("B6", i, 0), "Rodikliai".decode("utf8"), self.header_style)
        self.ws.write(self.inc("B7", i, 0), "ISSN".decode("utf8"), self.header_style)
        self.ws.write(self.inc("B8", i, 0), "ISBN".decode("utf8"), self.header_style)
        self.ws.write(self.inc("B9", i, 0), "Žurnalas".decode("utf8"), self.header_style)
        self.ws.write(self.inc("B10", i, 0), "Nouroda".decode("utf8"), self.header_style)
        self.ws.write(self.inc("B11", i, 0), "Pastabos".decode("utf8"), self.header_style)
        for n in range(10):
            self.ws.write(self.inc("C5", i, n), None, self.pub_style)
            self.ws.write(self.inc("C6", i, n), None, self.pub_style)

    def inc(self, xy, row, col):
        if ExcelWriter.is_coordinate(xy):
            return ExcelWriter.__inc(xy, row, col)
        if ExcelWriter.is_range(xy):
            a, b = xy.split(":")
            a = self.__inc(a, row, col)
            b = self.__inc(b, row, col)
            return a + ":" + b
        raise RuntimeError("Coordinate error!")

    @staticmethod
    def __inc(xy, r, c):
        if ExcelWriter.is_coordinate(xy):
            row, col = xl_cell_to_rowcol(xy)
            return xl_rowcol_to_cell(row+r, col+c)

    @staticmethod
    def is_range(range_coordinates):
        regex = re.compile(r"^[a-z|A-Z]+[0-9]+:[a-z|A-Z]+[0-9]+$")
        if regex.match(range_coordinates):
            return True
        return False

    @staticmethod
    def is_coordinate(coordinate):
        regex = re.compile(r"^[a-z|A-Z]+[0-9]+$")
        if regex.match(coordinate):
            return True
        return False
