

class Selectors(object):
    x_doc_elements = "/html[@xmlns=\"http://www.w3.org/1999/xhtml\"]/body[@dir=\"ltr\"]/table[@border=\"0\"]" \
              "/tr[*]/td[2]/table[@border=\"0\"]/tr[@class]/td[2]/p[@class=\"param_20_value\"]"

    x_text = "text()"
    x_link = "*/text()"

    x_first_result = "//*[@id=\"___gcse_0\"]/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/" \
                     "table/tbody/tr/td[2]/div[1]/a"

    c_table = "table-responsive"
    x_elements = "./table/tbody/tr[position()>1 and position()<7]/td[position() < 3]"
