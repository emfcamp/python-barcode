# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""barcode.writer.svg

"""

import codecs
import gzip
import os
import xml.dom

from barcode import __version__
from .writerbase import BaseWriter


SIZE = '{0:.3f}mm'
COMMENT = 'Autogenerated from pyBarcode {0}'.format(__version__)


def _set_attributes(element, **attributes):
    for key, value in attributes.items():
        element.setAttribute(key, value)


def create_svg_object():
    imp = xml.dom.getDOMImplementation()
    doctype = imp.createDocumentType(
        'svg',
        '-//W3C//DTD SVG 1.1//EN',
        'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd'
    )
    document = imp.createDocument(None, 'svg', doctype)
    _set_attributes(document.documentElement, version='1.1',
                    xmlns='http://www.w3.org/2000/svg')
    return document


class SVGWriter(BaseWriter):

    def __init__(self):
        BaseWriter.__init__(self, self._init, self._create_module,
                            self._create_text, self._finish)
        self.compress = False
        self._document = None
        self._root = None

    def _init(self, code):
        self._document = create_svg_object()
        self._root = self._document.documentElement
        self._root.appendChild(self._document.createComment(COMMENT))

    def _create_module(self, xpos, ypos, width, color):
        element = self._document.createElement('rect')
        attributes = dict(x=SIZE.format(xpos), y=SIZE.format(ypos),
                          width=SIZE.format(width),
                          height=SIZE.format(self.module_height),
                          style='fill:{0};'.format(color))
        _set_attributes(element, **attributes)
        self._root.appendChild(element)

    def _create_text(self, xpos, ypos):
        element = self._document.createElement('text')
        attributes = dict(x=SIZE.format(xpos), y=SIZE.format(ypos),
                          style='fill:{0};font-size:{1}pt;text-anchor:'
                                'middle;'.format(self.foreground,
                                                 self.font_size))
        _set_attributes(element, **attributes)
        text_element = self._document.createTextNode(self.text)
        element.appendChild(text_element)
        self._root.appendChild(element)

    def _finish(self):
        if self.compress:
            return self._document.toxml(encoding='UTF-8')
        else:
            return self._document.toprettyxml(indent=4*' ', newl=os.linesep,
                                              encoding='UTF-8')

    def save(self, filename, output):
        if self.compress:
            _filename = '{0}.svgz'.format(filename)
            f = gzip.open(_filename, 'wb')
            f.write(output)
            f.close()
        else:
            _filename = '{0}.svg'.format(filename)
            with codecs.open(_filename, 'w', 'utf-8') as f:
                f.write(output)
        return _filename
