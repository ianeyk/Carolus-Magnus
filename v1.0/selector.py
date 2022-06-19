import pygame
from selectable import Selectable

class Selector():

    spacing = 1.5

    def __init__(self, my_class, x, y, size, ordinal_list):
        self.my_class = my_class
        self.x = x
        self.y = y
        self.ordinal_list = ordinal_list
        self.nItems = len(self.ordinal_list)
        self.size = size
        self.prev_selected_item = 0

        self.item_locs = self.generate_locs()
        self.item_list = [] # list of self.my_class objects for highlighting purposes
        for loc, ordinal_id in zip(self.item_locs, self.ordinal_list):
            item = self.my_class(*loc, ordinal_id)
            self.item_list.append(item)

    def draw(self, group):
        for item in self.item_list:
            item.add(group)

    def generate_locs(self):
        locs = []
        for pos in range(self.nItems):
            locs.append((self.x + (pos - self.nItems // 2) * self.my_class.size[0] * self.spacing, self.y + self.my_class.size[1] / 2))
        return locs

    def select(self, which_item): # which_item is an index from 0 to 6, indicating which item in the cache has been selected
        # updated_rects = self.deselect_all() # unhighlight all items
        updated_rects = self.item_list[self.prev_selected_item].un_highlight() # unhighlight the previous item
        updated_rects.extend(self.item_list[which_item].highlight()) # then highlight the interesting item
        self.prev_selected_item = which_item
        return updated_rects # returns the rect containing the highlighted item, for pygame.display.update() in the main loop

    def deselect_all(self):
        updated_rects = []
        for other_item in self.item_list:
            updated_rects.extend(other_item.un_highlight())
        return updated_rects