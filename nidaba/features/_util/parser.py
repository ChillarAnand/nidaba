import xml
from pyparsing import makeHTMLTags, SkipTo
try:
    from html.parser import HTMLParser
except:
    from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def tag_blocks(html_text, tag):
    tag_start, tag_end = makeHTMLTags(tag)
    tag_block = tag_start + SkipTo(tag_end).setResultsName('body') + tag_end
    for tokens, start, end in tag_block.scanString(html_text):
        yield tokens

def tag_container(html_text, tag):
    tag_container = ""
    for tag_block in tag_blocks(html_text, tag):
        tag_container += tag_block.body
    return tag_container

def code_text_ratio(html_text):
    text_size = len(strip_tags(html_text))
    tag_size = len(tag_container(html_text, 'code'))
    return tag_size/text_size
