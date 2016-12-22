import re


class RE(object):

    @staticmethod
    def is_latest(date):
        regex = re.compile(r"^[0-9]{4}/[0-9]{4}$")
        if regex.match(date):
            return True
        return False

    @staticmethod
    def is_publication(element):
        regex = re.compile(r"//\B(.*?)[.|:|/]")
        if regex.search(element):
            return True
        return False

    @staticmethod
    def is_link(element):
        regex = re.compile(r"<(.*?)>")
        if regex.match(element):
            return True
        return False
