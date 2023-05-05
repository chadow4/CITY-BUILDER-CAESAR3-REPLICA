from game.buildings import Building


class Engineers_Post(Building):

    def __init__(self, posx, posy):
        super().__init__(1, 1, posx, posy)

    def __repr__(self):
        return "Engineers_Post"

    #We still need to link it to engineers, in other words, to the walkers.
