import re
from datetime import date

def clean_string(string):
    return ' '.join(string.split())
def read_int(intString):
    return int(intString.translate({ord(','):""}))

def strip_label(info_string, label, i = 0, postprocess = lambda x:x, default = ""):
    if info_string[:len(label)] == label:
        return postprocess(info_string[len(label):]), i+1
    else:
        return default, i

def read_character_string(string):
    def clean_character_list(x):
        x2 = list(map(clean_string, x.translate({ord(']'):",", ord('['):""}).split(",")))
        if x2[-1] == '':
            return x2[:-1]
        return x2
    romances = map(clean_character_list, re.findall("\[.*?\]", string))
    characters = clean_character_list(string)
    return list(characters), list(romances)

def read_date(string):
	if string is None:
		return None
	x = string.split('-')
	return x# date(int(year), int(month), int(day))
