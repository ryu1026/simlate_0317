import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

random.seed(1234)


# define the class with the `make_not_gaussian_beads_not_overlap` method

class Beads:
    def __init__(self, num_beads, row_grid_size, col_grid_size, beads_diameter, grid_step, num_frames):
        self.num_beads = num_beads
        self.row_grid_size = row_grid_size
        self.col_grid_size = col_grid_size
        self.beads_diameter = beads_diameter
        self.grid_step = grid_step
        self.num_frames = num_frames
        self.shift_amounts = np.linspace(0, col_grid_size, num_frames + 1, endpoint=False, dtype=int)[1:]
        self.grid_row, self.grid_col = np.meshgrid(np.arange(0, self.row_grid_size, self.grid_step),
                                                   np.arange(0, self.col_grid_size, self.grid_step))

    def make_not_gaussian_beads_not_overlap(self, shift_amount=0, do_print=False):
        beads_col = []
        beads_row = []
        while len(beads_col) < self.num_beads:
            bead_col = np.random.randint(self.beads_diameter, self.col_grid_size - self.beads_diameter)
            bead_row = self.row_grid_size - np.random.randint(self.beads_diameter,
                                                              self.row_grid_size - self.beads_diameter)

            too_close = False
            for pre_col, pre_row in zip(beads_col, beads_row):
                if np.sqrt((bead_col - pre_col) ** 2 + (bead_row - pre_row) ** 2) < 2 * self.beads_diameter:
                    too_close = True
                    break

            if not too_close:
                beads_col.append(bead_col)
                beads_row.append(bead_row)

        # shift bead positions by shift_amount
        beads_col = [(col - shift_amount) % self.col_grid_size for col in beads_col]

        mask = np.zeros_like(self.grid_row)

        for bead_col, bead_row in zip(beads_col, beads_row):
            if do_print:
                print("beads_pos: (行, 列) = ({0}, {1}) = (y, x)".format(bead_col, bead_row))
            dist = np.sqrt((self.grid_col - bead_col) ** 2 + (self.grid_row - bead_row) ** 2)
            mask += dist < (self.beads_diameter / 2)
        beads_matrix = np.clip(mask, 0., 1.)

        return beads_matrix, beads_col, beads_row

    def make_not_gaussian_beads_not_overlap_ai(self, frame_idx, do_print=False):
        shift_amount = self.shift_amounts[frame_idx % self.num_frames]

        beads_col = []
        beads_row = []
        while len(beads_col) < self.num_beads:
            bead_col = np.random.randint(self.beads_diameter, self.col_grid_size - self.beads_diameter)
            bead_row = self.row_grid_size - np.random.randint(self.beads_diameter,
                                                              self.row_grid_size - self.beads_diameter)

            too_close = False
            for pre_col, pre_row in zip(beads_col, beads_row):
                if np.sqrt((bead_col - pre_col) ** 2 + (bead_row - pre_row) ** 2) < 2 * self.beads_diameter:
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

    def create_shifted_beads_matrix(self, num_shits):
        beads_matrices = []
        beads_cols = []
        beads_rows = []
        for shift_amount in range(num_shits):
            beads_matrix, beads_col, beads_row = self.make_not_gaussian_beads_not_overlap(shift_amount=shift_amount)
            beads_matrices.append(beads_matrix)
            beads_cols.append(beads_col)
            beads_rows.append(beads_row)

        shifted_beads_matrix = np.concatenate(beads_matrices, axis=1)

        return shifted_beads_matrix, beads_cols, beads_rows

    def move_beads_matrix(self, beads_matrix, shift_amount):
        """
        beads_matrixを列方向にのみ移動させる
        :param shift_amount:
        :return:
        """

# create the Beads object and set animation parameters
beads = Beads(num_beads=1, row_grid_size=100, col_grid_size=100, beads_diameter=10, grid_step=0.1)
beads_matrix, _, _ = beads.make_not_gaussian_beads_not_overlap()

fig, ax = plt.subplots()


# define the animation function
def animate(frame):
    global shift_amount
    ax.clear()
    beads_matrix, _, _ = beads.make_not_gaussian_beads_not_overlap(shift_amount=shift_amount, do_print=True)
    # shift_amount += 0.001
    ax.imshow(beads_matrix, cmap='gray', extent=(0, beads.row_grid_size, 0, beads.row_grid_size))
    ax.set_xlabel("row (microns)")
    ax.set_ylabel("col (microns")
    ax.xaxis.set_ticks_position('top')
    # ax.imshow(beads_matrix, cmap='gray_r', vmin=0, vmax=1, aspect='auto')
    # ax.set_axis_off()


def update(frame):
    # move the mask part of the beads matrix to the left
    shift_amount = -1 * frame
    shifted_beads_matrix = beads_matrix.copy()
    shifted_beads_matrix, _, _ = beads.make_not_gaussian_beads_not_overlap(shift_amount=shift_amount)

    # clear the axis and plot the shifted beads matrix
    ax.clear()
    ax.imshow(shifted_beads_matrix, cmap='gray', extent=(0, beads.row_grid_size, 0, beads.row_grid_size))
    # ax.imshow(shifted_beads_matrix, cmap='gray_r')


frames = beads.col_grid_size
# create the animation and display it
ani = animation.FuncAnimation(fig, update, frames=frames, interval=50)
plt.show()
