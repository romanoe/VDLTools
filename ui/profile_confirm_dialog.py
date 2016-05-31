# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VDLTools
                                 A QGIS plugin for the Ville de Lausanne
                              -------------------
        begin                : 2016-05-30
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

from PyQt4.QtGui import (QDialog, QGridLayout, QPushButton, QLabel)


class ProfileConfirmDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Edition Confirmation")
        self.resize(300, 100)
        self.__layout = QGridLayout()

        self.__confirmLabel = QLabel("")

        self.__layout.addWidget(self.__confirmLabel, 0, 0, 1, 2)

        self.__okButton = QPushButton("OK")
        self.__okButton.setMinimumHeight(20)
        self.__okButton.setMinimumWidth(100)

        self.__cancelButton = QPushButton("Cancel")
        self.__cancelButton.setMinimumHeight(20)
        self.__cancelButton.setMinimumWidth(100)

        self.__layout.addWidget(self.__okButton, 1, 1)
        self.__layout.addWidget(self.__cancelButton, 1, 2)

        self.setLayout(self.__layout)


    def setMessage(self, message):
        self.__confirmLabel.setText(message)

    def okButton(self):
        return self.__okButton

    def cancelButton(self):
        return self.__cancelButton
