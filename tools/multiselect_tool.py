# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VDLTools
                                 A QGIS plugin for the Ville de Lausanne
                              -------------------
        begin                : 2017-01-31
        git sha              : $Format:%H$
        copyright            : (C) 2016 Ville de Lausanne
        author               : Christophe Gusthiot
        email                : christophe.gusthiot@lausanne.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from __future__ import division
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QColor
from qgis.gui import (QgsMapTool,
                      QgsRubberBand)
from qgis.core import (QGis,
                       QgsWKBTypes,
                       QgsRectangle,
                       QgsMapLayer,
                       QgsLineStringV2,
                       QgsPolygonV2,
                       QgsPointV2,
                       QgsGeometry)


class MultiselectTool(QgsMapTool):
    """
    Map tool class to duplicate an object
    """

    def __init__(self, iface):
        """
        Constructor
        :param iface: interface
        """
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.__iface = iface
        self.__canvas = iface.mapCanvas()
        self.__icon_path = ':/plugins/VDLTools/icons/select_icon.png'
        self.__text = QCoreApplication.translate("VDLTools","Select features on multiple layers")
        self.__selecting = False
        self.__first = None
        self.__last = None
        self.__temp = None
        self.__rubber = None

    def activate(self):
        """
        When the action is selected
        """
        QgsMapTool.activate(self)
        self.__rubber = QgsRubberBand(self.__canvas, QGis.Polygon)
        color = QColor("red")
        color.setAlphaF(0.6)
        self.__rubber.setBorderColor(color)
        color = QColor("orange")
        color.setAlphaF(0.3)
        self.__rubber.setFillColor(color)

    def deactivate(self):
        """
        When the action is deselected
        """
        self.__rubber = None
        QgsMapTool.deactivate(self)

    def icon_path(self):
        """
        To get the icon path
        :return: icon path
        """
        return self.__icon_path

    def text(self):
        """
        To get the menu text
        :return: menu text
        """
        return self.__text

    def toolName(self):
        """
        To get the tool name
        :return: tool name
        """
        return QCoreApplication.translate("VDLTools","Multiselect")

    def setTool(self):
        """
        To set the current tool as this one
        """
        self.__canvas.setMapTool(self)

    def canvasMoveEvent(self, event):
        if self.__selecting:
            self.__temp = event.mapPoint()
            self.__rubber.reset()
            first = QgsPointV2(self.__first.x(), self.__first.y())
            second = QgsPointV2(self.__first.x(), self.__temp.y())
            third = QgsPointV2(self.__temp.x(), self.__temp.y())
            forth = QgsPointV2(self.__temp.x(), self.__first.y())

            lineV2 = QgsLineStringV2()
            lineV2.setPoints([first, second, third, forth, first])
            polygonV2 = QgsPolygonV2()
            polygonV2.setExteriorRing(lineV2)
            geom = QgsGeometry(polygonV2)
            self.__rubber.setToGeometry(geom, None)

    def canvasReleaseEvent(self, event):
        self.__selecting = False
        self.__last = event.mapPoint()
        self.__rubber.reset()
        types = [QgsWKBTypes.PointZ, QgsWKBTypes.LineStringZ, QgsWKBTypes.CircularStringZ, QgsWKBTypes.CompoundCurveZ,
                 QgsWKBTypes.CurvePolygonZ, QgsWKBTypes.PolygonZ]
        searchRect = QgsRectangle(self.__first, self.__last)
        for layer in self.__iface.mapCanvas().layers():
            if layer.type() == QgsMapLayer.VectorLayer and QGis.fromOldWkbType(layer.wkbType()) in types:
                layer.select(searchRect, False)
                if layer.selectedFeatureCount() > 0:
                    print(layer.name(), layer.selectedFeatureCount())

    def canvasPressEvent(self, event):
        self.__selecting = True
        self.__first = event.mapPoint()
