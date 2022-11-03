from mesa import Agent


class Cell(Agent):
    """Represents a single ALIVE or DEAD cell in the simulation."""

    DEAD = 0
    ALIVE = 1

    def __init__(self, pos, model, init_state=DEAD):
        """
        Create a cell, in the given state, at the given x, y position.
        """
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state
        self._nextState = None

    def isAlive(self):
        return self.state == self.ALIVE

    def isDead(self):
        return self.state == self.DEAD

    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def coord_x(self):
        return self.x

    def coord_y(self):
        return self.y

    def neighborStatus(self, list):
        if list[0].isDead() and list[1].isDead() and list[2].isAlive():
            return True
        elif list[0].isDead() and list[1].isAlive() and list[2].isAlive():
            return True
        elif list[0].isAlive() and list[1].isDead() and list[2].isDead():
            return True
        elif list[0].isAlive() and list[1].isAlive() and list[2].isDead():
            return True
        else:
            return False

    def step(self):
        """
        Compute if the cell will be dead or alive at the next tick.  This is
        based on the number of alive or dead neighbors.  The state is not
        changed here, but is just computed and stored in self._nextState,
        because our current state may still be necessary for our neighbors
        to calculate their next state.
        """

        # Get the neighbors and apply the rules on whether to be alive or dead
        # at the next tick.

        # live_neighbors = [neighbor.isAlive() for neighbor in self.neighbors()]

        # Assume nextState is unchanged, unless changed below.

        live_neighbors = [neighbor for neighbor in self.neighbors() if neighbor.coord_y() == (self.coord_y()+1) % 50]

        if self.neighborStatus(live_neighbors):
            self._nextState = self.ALIVE
        else:
            self._nextState = self.DEAD

    def advance(self):
        """
        Set the state to the new computed state -- computed in step().
        """
        self.state = self._nextState