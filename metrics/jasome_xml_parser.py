import xml.etree.ElementTree as et
from functools import reduce


def get_children_by_name(element, name):
    return filter(lambda e: e.tag.endswith(name), element.getchildren())


def get_elements_by_path(root, path):
    elements = [([], root)]
    for name in path:
        elements = reduce(list.__add__,
                          map(lambda elem: map(lambda child: (elem[0] + [child], child),
                                               get_children_by_name(elem[1], name)), elements), [])
    return elements

def parse(xml_path):
    root = et.parse(xml_path).getroot()
