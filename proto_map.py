#Generate prototype country data for testing gameplay
#Territories will be a grid of hexagons

class Proto_map:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.scale_x = 100
        self.scale_y = 100
        self.offset_x = 200
        self.offset_y = 150
        #self.territory = []
        self.all_territories = []
        self.build_proto_coords(self.rows, self.cols)

    def new_territory(self, row, col):
        #returns a set of polygon indexes comprising a new hex territory
        t = []
        y = row
        x = col
        ox = self.offset_x
        oy = self.offset_y
        sx = self.scale_x
        sy = self.scale_y
        if row%2 == 0: 
            ox = ox - .5 * sx 
        t.append(((ox + (.5 + x) * sx), (oy + (0 + y) * sy)))
        t.append(((ox + (1 + x) * sx), (oy + (.5 + y) * sy)))
        t.append(((ox + (1 + x) * sx), (oy + (1 + row) * sy)))
        t.append(((ox + (.5 + x) * sx), (oy + (1.5 + row) * sy)))
        t.append(((ox + (0 + x) * sx), (oy + (1 + row) * sy)))
        t.append(((ox + (0 + x) * sx), (oy + (.5 + row) * sy)))
        t.append(((ox + (.5 + x) * sx), (oy + (0 + y) * sy)))
        return t

    def build_proto_coords(self, rows, cols):
        ts = []
        for r in range(rows):
            for c in range(cols):
                territory = ["T"+str(r)+str(c)], self.new_territory(r, c)
                ts.append(territory)
                print(territory)
        print("Proto built")
        self.all_territories = ts
