import pygame as pg
from shapely.geometry import Point, Polygon
import proto_map

class Country:
    def __init__(self, name: str, coords: list) -> None:
        self.name = name
        self.coords = coords 
        self.font = pg.font.SysFont(None, 24)
        self.polygon = Polygon(self.coords)
        #self.center = self.get_center()
        self.color = (72, 126, 176)
        self.hovered = False

    def update(self, mouse_pos: pg.Vector2) -> None:
        self.hovered = False
        if Point(mouse_pos.x, mouse_pos.y).within(self.polygon):
            self.hovered = True

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.polygon(screen, (200, 126, 72) if self.hovered else self.color, self.coords)  #filled
        pg.draw.polygon(screen,(255, 255, 255), self.coords, width=1)  #outline

class World:
    def __init__(self, approach, proto_r, proto_c) -> None:
        self.approach = approach
        self.proto_r = proto_r
        self.proto_c = proto_c
        self.geo_data = self.read_geo_data()  #text name + coordinates
        self.countries = self.create_countries()  #Country objects
        self.hovered_country = None

    def read_geo_data(self) -> None:
        if self.approach == "Proto":
            proto_world = proto_map.Proto_map(self.proto_r, self.proto_c)
            print(proto_world)
            for t in proto_world.all_territories:
                print(str(t))
            return proto_world.all_territories
        else:
            pass  # Read countries from a data file

    def create_countries(self) -> None:
        countries = []
        for name, coords in self.geo_data:
            xy_coords = []
            for coord in coords:
                x = coord[0]
                y = coord[1]
                xy_coords.append(pg.Vector2(x, y))
            countries.append(Country(name, xy_coords))
            
            print(Country(name, xy_coords))
        return countries

    def draw(self, screen: pg.Surface) -> None:
        for country in self.countries:
            country.draw(screen)

    def update(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        self.hovered_country = None
        for country in self.countries:
            country.update(pg.Vector2(mouse_pos[0], mouse_pos[1]))
            if country.hovered:
                self.hovered_country = country