import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
import csv 
from PySide6.QtSvgWidgets import QGraphicsSvgItem

from ui_clientGUI import Ui_MainWindow

import sys
from collections import Counter
from random import choice, shuffle
from config import classic_territories, region_bonus, classic_cards, game_players, classic_army_center




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
        position = event.position()
        global scenePos
        scenePos = self.mapToScene(position.x(), position.y())   
        #print(f"Mouse click at scene coordinates: ({scenePos.x()}, {scenePos.y()})")
        super().mousePressEvent(event)


class Territory(qtw.QGraphicsItem):
    def __init__(self, _name, _coordinates, _window, _region, _adjacencies, _owner, _armies=0,_color=qtc.Qt.GlobalColor.gray, _center_point=None):
        super().__init__()
        self.name = _name
        self.coordinates = _coordinates    # list of QPointF
        self.window = _window  # Reference to the main window to update the status bar
        self.polygon = qtg.QPolygonF(_coordinates)
        self.color = _color
        self.region = _region
        self.adjacencies = _adjacencies
        self.owner = _owner
        self.armies = _armies
        self.armies_center_point  = _center_point if _center_point else self.calculateCenter()

    def boundingRect(self):
        return self.polygon.boundingRect()

    def shape(self):
        path = qtg.QPainterPath()
        path.addPolygon(self.polygon)
        return path
    
    def paint(self, painter, option, widget=None):        
        painter.setBrush(qtg.QBrush(self.color))
        painter.drawPolygon(self.polygon)
        # Draw the number of armies
        painter.setPen(qtg.QPen(qtc.Qt.GlobalColor.black))  # Set text color
        painter.setFont(qtg.QFont("Arial", 10))  # Set text font and size
        # Calculate text width and height to properly center it
        text = str(self.armies)
        metrics = painter.fontMetrics()
        textWidth = metrics.horizontalAdvance(text)
        textHeight = metrics.height()
        # Adjusted text position to center the text
        textPos = qtc.QPointF(self.armies_center_point.x() - textWidth / 2, self.armies_center_point.y() - textHeight / 2 + metrics.ascent())
        # Painter number of armies
        painter.drawText(textPos, str(self.armies))  # Draw text at the calculated center point
        
    def mousePressEvent(self, event):
        print('Clicked on ', self.name)
        #position = event.position()
        #scenePos = self.mapToScene(position.x(), position.y())           
        #print(f"Mouse click at scene coordinates: ({scenePos.x()}, {scenePos.y()})")        
        #plot_and_log_point(scenePos, self.name)
        #self.changeColor(qtc.Qt.GlobalColor.red)
        #self.update()
        # TODO: Figure out how to get status bar working
        #self.window.setStatusMessage(f"{self.name} was clicked!")  # Update the status bar message

    def changeColor(self, new_color):
        self.color = new_color

    def calculateCenter(self):
        # Calculate the centroid of the polygon for placing the army count text
        if not self.coordinates:
            return qtc.QPointF(0, 0)
        x = sum(point.x() for point in self.coordinates) / len(self.coordinates)
        y = sum(point.y() for point in self.coordinates) / len(self.coordinates)
        #return qtc.QPointF(x, y)
        return qtc.QPointF(0, 0)



class Player:
    def __init__(self, _name, _color):
        self.name = _name
        self.color = _color


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
        # Overrides mapview created by Designer
        # TODO: Do this properly
        self.mapView = CustomGraphicsView(self.centralwidget)
        self.mapView.setObjectName(u"mapView")
        self.mapView.setGeometry(qtc.QRect(0, 10, 961, 761))
        self.mapScene = qtw.QGraphicsScene()
        self.mapView.setScene(self.mapScene)
        
        self.players = self.load_players()
        self.territories = self.load_territories()
        #self.test_adj()        # test all adjacencies are valid territories  TODO: move to load territories
        self.load_cards()       # TODO: standardize on whether using methods or functions in init      
        self.flag_victory = False 
        self.setup_game()
        self.play_game()

        
    def setStatusMessage(self, message):
        #self.statusBar.showMessage(message)
        pass

    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:
        #print(event.pos())
        pass
        return super().mousePressEvent(event)

    def load_map(self):
        # Use to load csv contents to list of tuples (country, QPointF objects for coordinates)
        # Returns dict {territory_name: [list of boundary coordinates]}
        csvfile = open('resources/countries.csv', newline='')
        c = csv.reader(csvfile)
        data = []
        for row in c:
            data.append([row[0], (float(row[1]), float(row[2]))])    
        territories = list(set([x[0] for x in data]))
        map = {}
        for territory in territories:
            points = [x[1] for x in data if x[0] == territory]
            qpoints = []
            for point in points:
                qpoints.append(qtc.QPointF(point[0], point[1]))
            map[territory] = qpoints
        return map

    def load_players(self):
        players = {}
        for p in game_players:
            players[p[0]] = Player(p[0], p[1])
        return players
            
    def load_territories(self):
        # Returns dictionary of Territory objects
        # defaulting to classic countries TODO: need process to select a map
        map = self.load_map()
        territories = {}
        # classic_territories is list of lists [Region, Territory, [Adjacent Territories]] in config.py
        # Get center coordinate for show number of armies
        for t in classic_territories:    
            if t[1] in classic_army_center.keys():
                center = qtc.QPointF(float(classic_army_center[t[1]][0]), float(classic_army_center[t[1]][1]))   
            else:
                center = None
            # Get coordinates from countries.csv file 
            # TODO: incorporate coordinates into same config file as other game parameters
            #(self, _name, _coordinates, _window, _region, _adjacencies, _owner, _armies=0,_color=qtc.Qt.GlobalColor.gray):
            territory = Territory(t[1], map[t[1]], self, t[0], t[2], 'Vacant', _center_point = center)
            territories[t[1]] = territory
            self.mapScene.addItem(territory)
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
        self.setup_initial_armies()
        self.statusBar().showMessage("Game set up is complete")
    
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
                self.territories[t].changeColor(self.players[p].color)
                #self.territories[t].owner = self.players[p].color
                
                #print(self.territories[t].name, self.territories[t].owner, self.players[p].color, 
                #      len(list(t.name for t in self.territories.values() if t.owner=='Vacant')))
                if len(list(t.name for t in self.territories.values() if t.owner=='Vacant')) == 0:
                    flag_assign_territories = False
                    break
                #else:
                #    print(len(list(t.name for t in self.territories.values() if t.owner=='Vacant')))
        
    def setup_initial_armies(self):
        # Four player game has each player start with 30 armies
        for p in self.players.keys():
            armies = 30
            # Place two armies in each territory owned by player
            for t in [t.name for t in self.territories.values() if t.owner==p]:
                self.territories[t].armies = 2
                armies -= 2
            # Distribute remaining armies randomly across territories owned by player
            while armies > 0:
                t = choice(list(t.name for t in self.territories.values() if t.owner==p)) 
                self.territories[t].armies += 1
                armies -= 1
        
    def calc_reinforcements_from_territories(self, _player):
        return max(int(sum(1 for k, v in self.territories.items() if v.owner == _player)/3),3)
            
    def calc_reinforcements_from_regions(self, _player):
        result =  0
        # iterate thru list of unique regions
        for region in list(set({v.region for k, v in self.territories.items()})):
            # if sum of player territories in region = sum of all territories in region => get bonus
            total_region = list({v1.name for k1,v1 in self.territories.items() if v1.region == region})
            player_region = list({v1.name for k1,v1 in self.territories.items() if v1.region == region and v1.owner == _player})
            if player_region == total_region:
                result += region_bonus[region]  # region_bonus loaded from config.py 
        return result

    def exchange_cards(self, _player):
        result = 0
        # TODO: Add 2 army benefit if own card NOTE: some rules limit to max 2 armies per turn in
        player_cards = Counter([v.unit for k, v in self.deck.items() if v.owner == _player]).most_common()
        number_cards = Counter([v.unit for k, v in self.deck.items() if v.owner == _player]).total()
        number_wild_cards = Counter([v.unit for k, v in self.deck.items() if v.owner == _player])['All']
        if number_cards >= 3:
            # test if 3 or more of one unit
            if player_cards[0][1] + number_wild_cards >= 3:
                result = 5 
            # test if one of each unit
            elif len(player_cards) >= 3:
                result = 5 
        return result
        


    def play_game(self):

        turn_order = list(self.players.keys())
        shuffle(turn_order)
        while not self.flag_victory:
            for p in turn_order:
                self.statusBar().showMessage('It is ' + p + "'s turn")
                reinforcements_from_territories = self.calc_reinforcements_from_territories(p)
                self.numArmiesTerritories.setText(str(reinforcements_from_territories))
                reinforcements_from_regions = self.calc_reinforcements_from_regions(p)
                self.numArmiesRegions.setText(str(reinforcements_from_regions))
                reinforcements_from_cards = self.exchange_cards(p)
                self.numArmiesCards.setText(str(reinforcements_from_cards))
                reinforcements_total = reinforcements_from_territories + reinforcements_from_regions + reinforcements_from_cards
                self.numTotalArmies.setText(str(reinforcements_total))
            self.flag_victory = True


        




if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = GameBoard()
    window.show()
    sys.exit(app.exec())
