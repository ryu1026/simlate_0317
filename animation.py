import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from beads import Beads


class BeadsAnimation:
    def __init__(self, num_beads, row_grid_size, col_grid_size, beads_diameter, grid_step):
        self.beads = Beads(num_beads, row_grid_size, col_grid_size, beads_diameter, grid_step)
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.beads.make_not_gaussian_beads_not_overlap()[0], cmap='gray')

    def update(self, i):
        beads_matrix, beads_col, beads_row = self.beads.make_not_gaussian_beads_not_overlap(shift_amount=i)
        self.im.set_data(beads_matrix)
        return [self.im]

    def animate(self):
        anim = FuncAnimation(self.fig, self.update, frames=self.beads.col_grid_size, interval=50, blit=True)
        plt.show()


if __name__ == '__main__':
    num_beads = 5
    row_grid_size = 200
    col_grid_size = 200
    beads_diameter = 15
    grid_step = 1

    beads_animation = BeadsAnimation(num_beads, row_grid_size, col_grid_size, beads_diameter, grid_step)
    beads_animation.animate()
