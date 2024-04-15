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
from random import choice
from config import classic_territories, region_bonus, classic_cards, game_players

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
        #scenePos = self.mapToScene(event.pos())     # marked as deprecated
        position = event.position()
        scenePos = self.mapToScene(position.x(), position.y())   
        #print(f"Mouse click at scene coordinates: ({scenePos.x()}, {scenePos.y()})")
        super().mousePressEvent(event)


class CountryItem(qtw.QGraphicsItem):
    def __init__(self, name, points, window, color=qtc.Qt.GlobalColor.gray):
        super().__init__()
        self.name = name
        self.points = points    # list of QPointF
        self.window = window  # Reference to the main window to update the status bar
        self.polygon = qtg.QPolygonF(points)
        self.color = color

    def boundingRect(self):
        return self.polygon.boundingRect()

    def shape(self):
        path = qtg.QPainterPath()
        path.addPolygon(self.polygon)
        return path
    
    def paint(self, painter, option, widget=None):        
        painter.setBrush(qtg.QBrush(self.color))
        painter.drawPolygon(self.polygon)
        

    def mousePressEvent(self, event):
        print('Clicked on ', self.name)
        #self.changeColor(qtc.Qt.GlobalColor.red)
        #self.update()
        # TODO: Figure out how to get status bar working
        #self.window.setStatusMessage(f"{self.name} was clicked!")  # Update the status bar message

    def changeColor(self, new_color):
        self.color = new_color


class Player:
    def __init__(self, _name, _color):
        self.name = _name
        self.color = _color


class Territory:
    def __init__(self, _name, _region, _adjacencies, _coordinates, _owner):
        self.name = _name
        self.region = _region
        self.adjacencies = _adjacencies
        self.owner = _owner
        self.coordinates = _coordinates
        self.armies = 0
        self.color = 'Blue'


class Card:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
        self.owner = 'Deck'



class GameBoard(qtw.QMainWindow, Ui_MainWindow):
    # Start with loading game parameters from a config file
    #   Later can accept game parameters from adminGUI
    def __init__(self):
        super().__init__()
        self.setupUi(self)              
        self.players = self.load_players()
        self.territories = self.load_territories()
        #self.test_adj()        # test all adjacencies are valid territories  TODO: move to load territories
        self.load_cards()       # TODO: standardize on whether using methods or functions in init
        
        # Overrides mapview created by Designer
        # TODO: how do this properly
        self.mapView = CustomGraphicsView(self.centralwidget)
        self.mapView.setObjectName(u"mapView")
        self.mapView.setGeometry(qtc.QRect(0, 10, 961, 761))
        
        self.mapScene = qtw.QGraphicsScene()
        self.mapView.setScene(self.mapScene)
        #self.mapView.setFixedSize(800, 600)        # Set in Designer

        # Adding countries (or other items) to the map
        self.addCountriesToMap()
        self.flag_victory = False 

        #self.setup_game()

        


    def addCountriesToMap(self):
        for name in self.territories:
            ter = CountryItem(name, self.territories[name].coordinates, self)
            self.mapScene.addItem(ter)

    def setStatusMessage(self, message):
        #self.statusBar.showMessage(message)
        pass

    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:
        #print(event.pos())
        pass
        return super().mousePressEvent(event)

    def load_map(self):
        #Use to load csv contents to list of tuples (country, QPointF objects for coordinates)
        csvfile = open('resources/countries.csv', newline='')
        c = csv.reader(csvfile)
        data = []
        for row in c:
            data.append([row[0], (float(row[1]), float(row[2]))])    
        territories = list(set([x[0] for x in data]))
        #coords = []
        map = {}
        for territory in territories:
            points = [x[1] for x in data if x[0] == territory]
            qpoints = []
            for point in points:
                qpoints.append(qtc.QPointF(point[0], point[1]))
            #coords.append((country, qpoints))
            map[territory] = qpoints
        return map

    def load_players(self):
        players = {}
        for p in game_players:
            players[p[0]] = Player(p[0], p[1])
        return players
            
    def load_territories(self):
        # defaulting to classic countries TODO: need process to select a map
        map = self.load_map()
        territories = {}
        # classic_territories is list of lists [Region, Territory, [Adjacent Territories]] in config.py
        for t in classic_territories:       
            # Get coordinates from countries.csv file 
            # TODO: incorporate coordinates into same config file as other game parameters
            territory = Territory(t[1], t[0], t[2], map[t[1]], 'Vacant')
            territories[t[1]] = territory
        return territories

    def test_adj(self):
        # Purpose is to confirm all adjacencies are valid territories
        for t in self.territories:
            for a in self.territories[t].adjacencies:
                if a in self.territories:
                    print(t, a)
                else:
                    print("Error - ", a)

    def load_cards(self):
        self.deck = {}
        for c in classic_cards:
            self.deck[c[0]] = Card(c[0], c[1])
        
    def setup_game(self):
        self.setup_territories()

    
    def setup_territories(self):
        player_names = self.players.keys()
        #territory_names = list(self.territories.keys())
        #territory_names = list(t.name for t in self.territories.values() if t.owner=='Vacant')
        flag_assign_territories = True
        while flag_assign_territories:
            for p in player_names:
                #print(choice(list(t.name for t in self.territories.values() if t.owner=='Vacant')))
                #sys.exit()
                t = choice(list(t.name for t in self.territories.values() if t.owner=='Vacant'))
                self.territories[t].owner = p
                print(self.territories[t].name, self.territories[t].owner, len(list(t.name for t in self.territories.values() if t.owner=='Vacant')))
                if len(list(t.name for t in self.territories.values() if t.owner=='Vacant')) == 0:
                    flag_assign_territories = False
                    break
                else:
                    print(len(list(t.name for t in self.territories.values() if t.owner=='Vacant')))


    def play_game(self):
        print('hello')
        pass

    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = GameBoard()
    window.show()
    window.play_game()
    sys.exit(app.exec())
