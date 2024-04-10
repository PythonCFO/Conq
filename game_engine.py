import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
import csv 
from PySide6.QtSvgWidgets import QGraphicsSvgItem


from ui_clientGUI import Ui_MainWindow

# Test Turns stuff
import sys
from collections import Counter
import random
from config import classic_territories, region_bonus, cards

class CustomGraphicsView(qtw.QGraphicsView):
    def __init__(self, parent=None):
        super(CustomGraphicsView, self).__init__(parent)
        self.setRenderHints(qtg.QPainter.Antialiasing | qtg.QPainter.SmoothPixmapTransform)
        self._zoom = 0

    def wheelEvent(self, event: qtg.QWheelEvent):
        scaleFactor = 1.25

        # Zoom in
        if event.angleDelta().y() > 0:
            self.scale(scaleFactor, scaleFactor)
            self._zoom += 1
        # Zoom out
        elif event.angleDelta().y() < 0 :
            self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)
            self._zoom -= 1


    def mousePressEvent(self, event: qtg.QMouseEvent):
        # Convert the mouse click position to scene coordinates
        scenePos = self.mapToScene(event.pos())
        #print(f"Mouse click at scene coordinates: ({scenePos.x()}, {scenePos.y()})")
        if window.cbxAddCountries.isChecked():                
            plot_and_log_point(scenePos, window.linCountry.text())
        super().mousePressEvent(event)



class CountryItem(qtw.QGraphicsItem):
    def __init__(self, name, points, window):
        super().__init__()
        self.name = name
        self.points = points    # list of QPointF
        self.window = window  # Reference to the main window to update the status bar
        self.polygon = qtg.QPolygonF(points)

    def boundingRect(self):
        return self.polygon.boundingRect()

    def shape(self):
        path = qtg.QPainterPath()
        path.addPolygon(self.polygon)
        return path
    
    def paint(self, painter, option, widget=None):        
        # Should not need this
        painter.drawPolygon(self.polygon)
        

    def mousePressEvent(self, event):
        print('Clicked on ', self.name)
        # TODO: Figure out how to get status bar working
        #self.window.setStatusMessage(f"{self.name} was clicked!")  # Update the status bar message



class GameBoard(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)              

        # This capability is for making a map with SVG background
        #self.cbxAddCountries.stateChanged.connect(self.cbxAddCountryChanged)
        if self.cbxAddCountries.isChecked():
            self.linCountry.setEnabled(True)

        # Overrides mapview created by Designer
        # TODO: how do this properly
        self.mapView = CustomGraphicsView(self.centralwidget)
        self.mapView.setObjectName(u"mapView")
        self.mapView.setGeometry(qtc.QRect(0, 10, 961, 761))
        
        self.mapScene = qtw.QGraphicsScene()
        self.mapView.setScene(self.mapScene)
        #self.mapView.setFixedSize(800, 600)        # Set in Designer

        #map_coordinates = load_coordinates()
        country_coordinates = load_country_coordinates()
        

        # load SVG background
        #svgBackground = QGraphicsSvgItem('resources/Risk_board.svg')
        #svgBackground.setZValue(-100)
        #self.mapScene.addItem(svgBackground)


        # Adding countries (or other items) to the map
        self.addCountriesToMap(self.mapScene, country_coordinates)
        # Plot the country outlines of known countries (subset of map_coordinates)
        #self.country_names = list(set(x[0] for x in country_coordinates))
        #for name in self.country_names:
        #    points = [x[1] for x in country_coordinates if x[0] == name]
        #    self.plot_territory(name, points[0]) #TODO: Why is points creating a list ?

        #self.plot_coordinates(map_coordinates)

    def plot_territory(self, name, coords):    
        # Use this function to create a map.  It shows the actual coordinates that are used for borders
        pen = qtg.QPen(qtc.Qt.red)
        radius = 2
        for point in coords:
            self.mapScene.addEllipse(point.x() - radius, point.y() - radius, radius * 2, radius * 2, pen)

    
    # This function not needed once have svg capability
    #def plot_coordinates(self, coordinates):
    #    Unclear what this function
    #    pen = qtg.QPen(qtc.Qt.black)
    #    radius = 1  # Radius of the points
    #    for point in coordinates:
    #        self.mapScene.addEllipse(point[0] - radius, point[1] - radius, radius * 2, radius * 2, pen)
    

    def addCountriesToMap(self, mapScene, countries):
        for name, points in countries:
            country = CountryItem(name, points, self)
            mapScene.addItem(country)

    def setStatusMessage(self, message):
        #self.statusBar.showMessage(message)
        pass

    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:
        #print(event.pos())
        pass
        return super().mousePressEvent(event)

    def cbxAddCountryChanged(self, state):
        if state:
            self.linCountry.setEnabled(True)


def load_coordinates():
    #Use to load csv file of coordinates into a list
    csvfile = open('resources/map_coordinates_clean.csv', newline='')
    c = csv.reader(csvfile)
    coords = []
    for row in c:
        coords.append((float(row[0]), float(row[1])))
    return coords

def load_country_coordinates():
    #Use to load csv contents to list of tuples (country, QPointF objects for coordinates)
    csvfile = open('resources/countries.csv', newline='')
    c = csv.reader(csvfile)
    data = []
    for row in c:
        data.append([row[0], (float(row[1]), float(row[2]))])    
    countries = list(set([x[0] for x in data]))
    coords = []
    for country in countries:
        points = [x[1] for x in data if x[0] == country]
        qpoints = []
        for point in points:
            qpoints.append(qtc.QPointF(point[0], point[1]))
        coords.append((country, qpoints))
    return coords

def plot_and_log_point(scenePos, country_name):
    pen = qtg.QPen(qtc.Qt.blue)
    radius = 1
    window.mapScene.addEllipse(scenePos.x() - radius, scenePos.y() - radius, radius * 2, radius * 2, pen)
    # want to append to existing file
    with open('resources/countries.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([country_name, round(scenePos.x(),1), round(scenePos.y(),1)])





if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = GameBoard()
    window.show()
    sys.exit(app.exec())
