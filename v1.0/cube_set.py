class CubeSet():
    color_dict = {0:"green", 1:"red", 2:"blue", 3:"yellow", 4:"pink"}

    def __init__(self):
        self.cubes = [0, 0, 0, 0, 0]

    def add_cube(self, color_id):
        self.cubes[color_id] += 1

    def remove_cube(self, color_id):
        if self.cubes[color_id] <= 0:
            print("Tried to remove a cube when there are no cubes of that color")
        self.cubes[color_id] -= 1

    def get_cube_count(self, color_id):
        return self.cubes[color_id]

    def get_cubes(self):
        return self.cubes

    def add_cubeSet(self, other):
        for color_id in range(5):
            self.cubes[color_id] += other.cubes[color_id]

    def subtract_cubeSet(self, other):
        for color_id in range(5):
            self.cubes[color_id] -= other.cubes[color_id]

    def get_cube_list(self):
        cube_list = []
        for color_id, num_cubes in enumerate(self.cubes):
            cube_list.extend([color_id] * num_cubes)
        return cube_list


    def __repr__(self):
        string = "CubeSet <"
        initial_len = len(string)
        if self.cubes[0] > 0:
            string += str(self.cubes[0]) + " green, "
        if self.cubes[1] > 0:
            string += str(self.cubes[1]) + " red, "
        if self.cubes[2] > 0:
            string += str(self.cubes[2]) + " blue, "
        if self.cubes[3] > 0:
            string += str(self.cubes[3]) + " yellow, "
        if self.cubes[4] > 0:
            string += str(self.cubes[4]) + " pink, "

        if len(string) != initial_len: # at least one cube color was reported
            string = string[:-2] # chop off the last two characters (the ", ")
        string += ">"
        return string
