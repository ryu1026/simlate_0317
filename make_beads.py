import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

random.seed(1234)


# コンストラクタでグリッドと蛍光ビーズをつくっちゃってあとから動かすメソッドを追加してみる

class Beads:
    def __init__(self, num_beads, row_grid_size, col_grid_size, beads_diameter, grid_step, num_frames=100, do_print=True):
        self.num_beads = num_beads
        self.row_grid_size = row_grid_size
        self.col_grid_size = col_grid_size
        self.beads_diameter = beads_diameter
        self.grid_step = grid_step
        self.num_frames = num_frames
        self.grid_row, self.grid_col = np.meshgrid(np.arange(0, self.row_grid_size, self.grid_step),
                                                   np.arange(0, self.col_grid_size, self.grid_step))
        self.do_print = do_print

        beads_col = np.random.randint(self.beads_diameter, self.col_grid_size - self.beads_diameter, self.num_beads)
        # 列方向の位置を決定
        # beads_row = np.random.randint(0, self.row_grid_size, self.num_beads)
        beads_row = np.random.randint(self.beads_diameter, self.row_grid_size - self.beads_diameter,
                                      self.num_beads)
        mask = np.zeros_like(self.grid_row)
        # clipped_mask = np.zeros_like(self.grid_col)
        for bead_col, bead_row in zip(beads_col, beads_row):
            if do_print:
                # print("beads_pos: (行, 列) = ({0}, {1})".format(bead_col, abs(self.row_grid_size - bead_row)))
                print("beads_pos: (行, 列) = ({0}, {1}) = (y, x)".format(bead_col, bead_row))
            # ランダムに決定した中心と格子点の距離を計算
            dist = np.sqrt((self.grid_col - bead_col) ** 2 + (self.grid_row - bead_row) ** 2)
            # 現在のビーズの中心からself.beads_diameter/2 よりも近い全てのグリッド点で1に更新される
            mask += dist < (self.beads_diameter / 2)
        self.beads_matrix = np.clip(mask, 0., 1.)

    def move_beads_matrix(self, shift_amount):
        """
        beads_matrixを列方向にのみ移動させる
        :return:
        """
        shifted_beads_matrix = np.roll(self.beads_matrix, shift=shift_amount, axis=1)
        return shifted_beads_matrix

    def draw_not_gaussian_beads(self, not_gaussian_beads) -> object:
        fig, ax = plt.subplots()
        ax.imshow(not_gaussian_beads, cmap='gray', interpolation='nearest',
                  extent=(0, self.col_grid_size, 0, self.row_grid_size))
        ax.set_xlabel("row (microns)")
        ax.set_ylabel("col (microns)")
        ax.set_title("Not gaussian fluorescent beads")
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_label_position('top')
        # ax.invert_yaxis()
        plt.show()


# create the Beads object and set animation parameters
# Move the beads matrix
beads = Beads(num_beads=10, row_grid_size=100, col_grid_size=100, beads_diameter=10, grid_step=0.1)
# shifted_beads_matrix = beads.move_beads_matrix()

fig, ax = plt.subplots()
im = ax.imshow(beads.beads_matrix, cmap='gray', interpolation='nearest',
               extent=(0, beads.col_grid_size, 0, beads.row_grid_size))
ax.set_xlabel("row (microns)")
ax.set_ylabel("col (microns)")
# ax.xaxis.set_ticks_position('top')
# ax.xaxis.set_label_position('top')

for i in range(beads.num_frames):
    shifted_beads_matrix = beads.move_beads_matrix(shift_amount=10)
    im.set_data(shifted_beads_matrix)
    plt.pause(0.1)  # pause to allow animation to be seen
    beads.beads_matrix = shifted_beads_matrix

plt.show()


# if np.array_equal(beads.beads_matrix, shifted_beads_matrix):
#     print("Same")
# else:
#     print("Different")
# beads.draw_not_gaussian_beads(beads.beads_matrix)
# beads.draw_not_gaussian_beads(shifted_beads_matrix)


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

# frames = beads.col_grid_size
# # create the animation and display it
# ani = animation.FuncAnimation(fig, update, frames=frames, interval=50)
# plt.show()
