import xml.etree.ElementTree as et
from functools import reduce
import os
import pandas as pd

def get_children_by_name(element, name):
    return list(filter(lambda e: e.tag.endswith(name), element.getchildren()))


def get_elements_by_path(root, path):
    elements = [([], root)]
    for name in path:
        elements = reduce(list.__add__,
                          map(lambda elem: list(map(lambda child: (elem[0] + [child], child),
                                               get_children_by_name(elem[1], name))), elements), [])
    return list(elements)


def parse(xml_path):
    root = et.parse(xml_path).getroot()
    classes_metrics = []
    methods_metrics = []
    for klass_path, klass in get_elements_by_path(root, ['Packages', 'Package', 'Classes', 'Class']):
        source_file = os.path.normpath(klass.attrib['sourceFile'])
        class_path = klass_path[1].attrib['name'] + '.' + klass.attrib['name']
        class_metrics = {"Class Path": class_path}
        for metric_path, metric in get_elements_by_path(klass, ['Metrics', 'Metric']):
            class_metrics[metric.attrib['name']] = metric.attrib['value']
        classes_metrics.append(class_metrics)
        for method_path, method in get_elements_by_path(klass, ['Methods', 'Method']):
            method_metrics = {"File Name": source_file,'start_line': int(method.attrib['lineStart'])}
            for metric_path, metric in get_elements_by_path(method, ['Metrics', 'Metric']):
                method_metrics[metric.attrib['name']] = metric.attrib['value']
            methods_metrics.append(method_metrics)
    return pd.DataFrame(classes_metrics), pd.DataFrame(methods_metrics)
