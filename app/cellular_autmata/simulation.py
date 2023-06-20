import numpy as np
import cv2
from scipy import signal

OCEAN_BLUE = np.array([0, 157, 196], np.uint8)
MIN_VISUAL_OIL_AMOUNT = 0.001

class CellularAutomata:
    def __init__(self, height, width, oil_starting_point, oil_starting_amount) -> None:
        self.height = height
        self.width = width
        self.m = 0.0014 # dispersion coeff
        self.d = 0.18 # diagonal coeff
        self.cells = np.zeros(shape=(height, width), dtype=np.float32)
        self.cells[oil_starting_point[0], oil_starting_point[1]] = oil_starting_amount

    def run_simulation(self, n):
        dispersion_convolution_mask = self.__get_dispersion_convolution_mask()
        self.show(0)
        for i in range(n):
            change = signal.convolve2d(self.cells, dispersion_convolution_mask, mode="same")
            self.cells += change
            self.show(i + 1)


    def __get_dispersion_convolution_mask(self):
        corner = self.m * self.d
        edge = self.m
        center = -4 * edge + -4 * corner
        return np.array([[corner, edge,  corner],
                         [edge,   center,  edge],
                         [corner, edge,  corner]], dtype=np.float32)
            
    def show(self, step):
        I = np.zeros((self.height, self.width, 3), np.uint8)
        I_binary = np.zeros((self.height, self.width, 3), np.uint8)

        # oil_patch = np.sqrt(self.cells) / np.sqrt(np.max(self.cells))
        # oil_patch = np.nan_to_num(oil_patch)
        oil_patch = self.cells.copy().astype('float32')
        oil_patch[oil_patch > MIN_VISUAL_OIL_AMOUNT] = np.maximum(oil_patch[oil_patch > MIN_VISUAL_OIL_AMOUNT], 10)
        oil_patch /= oil_patch.max()
        oil_patch = (1 - oil_patch)

        I[:, :, :] = oil_patch[:, :, np.newaxis] * OCEAN_BLUE
        I_binary[:, :, :] = (self.cells[:, :, np.newaxis] <= MIN_VISUAL_OIL_AMOUNT).astype('uint8') * OCEAN_BLUE

        I = cv2.cvtColor(I, cv2.COLOR_RGB2BGR)
        I_binary = cv2.cvtColor(I_binary, cv2.COLOR_RGB2BGR)

        cv2.putText(I, str(step), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(I_binary, str(step), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

        I = cv2.resize(I, (self.width * 3, self.height * 3), interpolation = cv2.INTER_NEAREST)
        I_binary = cv2.resize(I_binary, (self.width * 3, self.height * 3), interpolation = cv2.INTER_NEAREST)

        cv2.imshow('Cellular Autamta', I)
        cv2.imshow('Cellular Autamta Binary', I_binary)
        cv2.waitKey(1)
