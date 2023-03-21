import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# define the class with the `make_not_gaussian_beads_not_overlap` method

class Beads:
    def __init__(self, num_beads, row_grid_size, col_grid_size, beads_diameter):
        self.num_beads = num_beads
        self.row_grid_size = row_grid_size
        self.col_grid_size = col_grid_size
        self.beads_diameter = beads_diameter
        self.grid_row, self.grid_col = np.mgrid[0:self.row_grid_size, 0:self.col_grid_size]

    def make_not_gaussian_beads_not_overlap(self, shift_amount=0, do_print=False):
        beads_col = []
        beads_row = []
        while len(beads_col) < self.num_beads:
            bead_col = np.random.randint(self.beads_diameter, self.col_grid_size - self.beads_diameter)
            bead_row = self.row_grid_size - np.random.randint(self.beads_diameter, self.row_grid_size-self.beads_diameter)

            too_close = False
            for pre_col, pre_row in zip(beads_col, beads_row):
                if np.sqrt((bead_col - pre_col)**2 + (bead_row - pre_row)**2) < 2 * self.beads_diameter:
                    too_close = True
                    break

            if not too_close:
                beads_col.append(bead_col)
                beads_row.append(bead_row)

        # shift bead positions by shift_amount
        beads_col = [(col + shift_amount) % self.col_grid_size for col in beads_col]

        mask = np.zeros_like(self.grid_row)

        for bead_col, bead_row in zip(beads_col, beads_row):
            if do_print:
                print("beads_pos: (行, 列) = ({0}, {1}) = (y, x)".format(bead_col, bead_row))
            dist = np.sqrt((self.grid_col - bead_col) ** 2 + (self.grid_row - bead_row) ** 2)
            mask += dist < (self.beads_diameter / 2)
        beads_matrix = np.clip(mask, 0., 1.)

        return beads_matrix, beads_col, beads_row

# create the Beads object and set animation parameters
beads = Beads(num_beads=10, row_grid_size=100, col_grid_size=100, beads_diameter=10)
shift_amount = 0
fig, ax = plt.subplots()

# define the animation function
def animate(frame):
    global shift_amount
    ax.clear()
    beads_matrix, _, _ = beads.make_not_gaussian_beads_not_overlap(shift_amount=shift_amount)
    shift_amount += 0.05
    ax.imshow(beads_matrix, cmap='gray_r', vmin=0, vmax=1, aspect='auto')
    ax.set_axis_off()

# create the animation and display it
ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()
