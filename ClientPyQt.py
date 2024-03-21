import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem
from PyQt6.QtGui import QPolygonF, QColor, QPen, QBrush, QPainter, QPixmap
from PyQt6.QtCore import Qt, QPointF

class HoverPolygonItem(QGraphicsPolygonItem):
    def __init__(self, polygon):
        super().__init__(polygon)
        self.setAcceptHoverEvents(True)
        self.defaultBrush = self.brush()
        self.hovering = False

    def hoverEnterEvent(self, event):
        self.hovering = True
        self.setBrush(QColor("green"))

    def hoverLeaveEvent(self, event):
        self.hovering = False
        self.setBrush(self.defaultBrush)

    def hoverMoveEvent(self, event):
        if self.isUnderMouse():
            if not self.hovering:
                self.hoverEnterEvent(event)
        else:
            if self.hovering:
                self.hoverLeaveEvent(event)

class PolygonWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polygon Drawing")
        self.setGeometry(100, 100, 800, 600)

        scene = QGraphicsScene()
        view = QGraphicsView(scene)
        self.setCentralWidget(view)

        #polygons = QGraphicsPolygonItem()
        polygon1 = HoverPolygonItem(QPolygonF(
            [
            QPointF(100, 100),
            QPointF(200, 100),
            QPointF(300, 150),
            QPointF(200, 200),
            QPointF(100, 200)
            ]),
            QPen(Qt.darkGreen),
        )
        polygon1.setBrush(QColor("red"))  # Set fill color to red
        scene.addItem(polygon1)

        polygon2 = HoverPolygonItem(QPolygonF([
            QPointF(200, 200),
            QPointF(300, 200),
            QPointF(300, 300),
            QPointF(200, 300)
        ]))
        polygon2.setBrush(QColor("red"))  # Set fill color to red
        scene.addItem(polygon2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PolygonWindow()
    window.show()
    sys.exit(app.exec())
