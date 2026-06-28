import cv2
import numpy as np
import os

# Số ô vuông, không phải inner corners
squares_x = 10
squares_y = 7

# Kích thước mỗi ô tính theo pixel
square_px = 100

img_w = squares_x * square_px
img_h = squares_y * square_px

checkerboard = np.ones((img_h, img_w), dtype=np.uint8) * 255

for y in range(squares_y):
    for x in range(squares_x):
        if (x + y) % 2 == 0:
            cv2.rectangle(
                checkerboard,
                (x * square_px, y * square_px),
                ((x + 1) * square_px, (y + 1) * square_px),
                0,
                -1
            )

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "checkerboard_10x7_squares_9x6_inner_corners.png")

cv2.imwrite(output_path, checkerboard)

print(f"Saved checkerboard image to: {output_path}")
