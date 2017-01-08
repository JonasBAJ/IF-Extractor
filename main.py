from __future__ import print_function

import Tkinter
import os
import sys
from tkFileDialog import askopenfilename

from api.Excel import ExcelWriter
from api.Web import WebDriverAPI
from parsers.DocParser import CSVParser
from parsers.Paths import Selectors
from vu.Regex import RE

QUERY_URL = "http://www.bioxbio.com/if/?q="
SAVE_LOCATION = ""


def main():
    tk_root = Tkinter.Tk()
    tk_root.withdraw()
    tk_root.update()
    f_path = askopenfilename(filetypes=[("Foos", "*.xlsx")])
    if f_path:
        if is_csv_file(f_path):
            parser = CSVParser(f_path)
            pubs = parser.get_pubs()
            start(pubs)
            write_excel(pubs)
            print("\n\nYour file was saved: " + SAVE_LOCATION)
            raw_input("Press Enter to end the program...")
        else:
            print("Not XML file!")
    else:
        print("File not selected!")


def start(pubs):
    operator = WebDriverAPI()
    operator.click_condition = lambda: operator.get_tabs_count() > 1
    try:
        surfer(operator, pubs)
    finally:
        operator.quit()


def surfer(operator, pubs):
    counter = float(0)
    end = float(len(pubs) - 1)
    for p in pubs:
        progress_bar(counter, end)
        if p.issn:
            p.IF, p.AIF = navigator(operator, p.issn)
        counter += 1


def navigator(operator, query):
    operator.get(QUERY_URL + query)
    e_link = operator.get_xpath_e(Selectors.x_first_result)
    try:
        if e_link:
            operator.click(e_link, 2)
            if operator.switch_to_tab(1):
                e_table = operator.get_class_e(Selectors.c_table)
                if e_table:
                    return extract(e_table.find_elements_by_xpath(Selectors.x_elements))
        return None, None
    finally:
        operator.close_all_except_one(0)


def extract(t_elements):
    if len(t_elements) > 0:
        IF = AIF = years = 0
        for i in range(0, len(t_elements)-1, 2):
            impact_factor = to_float(t_elements[i + 1].text)
            if impact_factor:
                if RE.is_latest(t_elements[i].text):
                    IF = impact_factor
                AIF += impact_factor
                years += 1
        return IF, round(AIF/years, 3)
    return None, None


def write_excel(pubs):
    global SAVE_LOCATION
    SAVE_LOCATION = os.path.expanduser("~/Desktop/VU_publications.xlsx")
    e = ExcelWriter(SAVE_LOCATION)
    e.print_publications(pubs)
    e.close()


def is_csv_file(f_path):
    if os.path.exists(f_path) and os.path.isfile(f_path):
        file_name = os.path.split(f_path)[1]
        if os.path.splitext(file_name)[1] == ".xlsx":
            return True
    return False


def progress_bar(counter, end):
    progress = counter / end * 100
    sys.stdout.write("\rprogress: [%d%%]" % progress)
    sys.stdout.flush()


def to_float(text):
    try:
        return float(text)
    except ValueError:
        return None

if __name__ == "__main__":
    main()
