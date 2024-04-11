# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mapBuilder.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGraphicsView,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1340, 966)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.armyDisplay = QFrame(self.centralwidget)
        self.armyDisplay.setObjectName(u"armyDisplay")
        self.armyDisplay.setGeometry(QRect(970, 60, 321, 381))
        self.armyDisplay.setFrameShape(QFrame.StyledPanel)
        self.armyDisplay.setFrameShadow(QFrame.Raised)
        self.armiesTitle = QLabel(self.armyDisplay)
        self.armiesTitle.setObjectName(u"armiesTitle")
        self.armiesTitle.setGeometry(QRect(10, 10, 301, 51))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.armiesTitle.setFont(font)
        self.armiesTitle.setTextFormat(Qt.MarkdownText)
        self.armiesTitle.setAlignment(Qt.AlignCenter)
        self.lblArmiesTerritories = QLabel(self.armyDisplay)
        self.lblArmiesTerritories.setObjectName(u"lblArmiesTerritories")
        self.lblArmiesTerritories.setGeometry(QRect(10, 80, 201, 41))
        self.lblArmiesTerritories.setFont(font)
        self.lblArmiesRegions = QLabel(self.armyDisplay)
        self.lblArmiesRegions.setObjectName(u"lblArmiesRegions")
        self.lblArmiesRegions.setGeometry(QRect(10, 120, 231, 41))
        self.lblArmiesRegions.setFont(font)
        self.lblArmiesCards = QLabel(self.armyDisplay)
        self.lblArmiesCards.setObjectName(u"lblArmiesCards")
        self.lblArmiesCards.setGeometry(QRect(10, 160, 201, 41))
        self.lblArmiesCards.setFont(font)
        self.numArmiesTerritories = QLabel(self.armyDisplay)
        self.numArmiesTerritories.setObjectName(u"numArmiesTerritories")
        self.numArmiesTerritories.setGeometry(QRect(250, 80, 51, 41))
        self.numArmiesTerritories.setFont(font)
        self.numArmiesTerritories.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.numArmiesRegions = QLabel(self.armyDisplay)
        self.numArmiesRegions.setObjectName(u"numArmiesRegions")
        self.numArmiesRegions.setGeometry(QRect(250, 120, 51, 41))
        self.numArmiesRegions.setFont(font)
        self.numArmiesRegions.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.numArmiesCards = QLabel(self.armyDisplay)
        self.numArmiesCards.setObjectName(u"numArmiesCards")
        self.numArmiesCards.setGeometry(QRect(250, 160, 51, 41))
        self.numArmiesCards.setFont(font)
        self.numArmiesCards.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lblTotalArmies = QLabel(self.armyDisplay)
        self.lblTotalArmies.setObjectName(u"lblTotalArmies")
        self.lblTotalArmies.setGeometry(QRect(10, 199, 201, 41))
        self.lblTotalArmies.setFont(font)
        self.numTotalArmies = QLabel(self.armyDisplay)
        self.numTotalArmies.setObjectName(u"numTotalArmies")
        self.numTotalArmies.setGeometry(QRect(250, 200, 51, 41))
        self.numTotalArmies.setFont(font)
        self.numTotalArmies.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.cardDisplay = QFrame(self.centralwidget)
        self.cardDisplay.setObjectName(u"cardDisplay")
        self.cardDisplay.setGeometry(QRect(970, 460, 321, 311))
        self.cardDisplay.setFrameShape(QFrame.StyledPanel)
        self.cardDisplay.setFrameShadow(QFrame.Raised)
        self.mapView = QGraphicsView(self.centralwidget)
        self.mapView.setObjectName(u"mapView")
        self.mapView.setGeometry(QRect(0, 10, 961, 761))
        self.cbxAddCountries = QCheckBox(self.centralwidget)
        self.cbxAddCountries.setObjectName(u"cbxAddCountries")
        self.cbxAddCountries.setGeometry(QRect(970, 10, 111, 20))
        self.linCountry = QLineEdit(self.centralwidget)
        self.linCountry.setObjectName(u"linCountry")
        self.linCountry.setEnabled(False)
        self.linCountry.setGeometry(QRect(1110, 8, 181, 22))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1340, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Game Board", None))
        self.armiesTitle.setText(QCoreApplication.translate("MainWindow", u"Armies", None))
        self.lblArmiesTerritories.setText(QCoreApplication.translate("MainWindow", u"Armies from Territories:", None))
        self.lblArmiesRegions.setText(QCoreApplication.translate("MainWindow", u"Armies from Regions:", None))
        self.lblArmiesCards.setText(QCoreApplication.translate("MainWindow", u"Armies from Cards:", None))
        self.numArmiesTerritories.setText(QCoreApplication.translate("MainWindow", u"15", None))
        self.numArmiesRegions.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.numArmiesCards.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblTotalArmies.setText(QCoreApplication.translate("MainWindow", u"Total Reinforcements:", None))
        self.numTotalArmies.setText(QCoreApplication.translate("MainWindow", u"17", None))
        self.cbxAddCountries.setText(QCoreApplication.translate("MainWindow", u"Add Countries", None))
    # retranslateUi

