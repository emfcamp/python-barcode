# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""barcode.writer.svg

"""
__docformat__ = 'restructuredtext en'

import os
import xml.dom
import zlib

from barcode import __version__
from barcode.writer.writerbase import BaseWriter


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

    def __init__(self, **options):
        BaseWriter.__init__(self, self._create_module, self._create_text,
                            self._finish)
        self.compress = False
        self.set_options(**options)
        #self._document = DOCUMENT
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
        data = self._document.createTextNode(self.text)
        element.appendChild(data)
        self._root.appendChild(element)

    def _finish(self):
        if self.compress:
            svg = self._document.toxml(encoding='UTF-8')
            svgz = zlib.compress(svg, 9)
            return ('svgz', svgz)
        else:
            svg = self._document.toprettyxml(indent=4*' ', newl=os.linesep,
                                             encoding='UTF-8')
            return ('svg', svg)
