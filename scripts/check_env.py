import cv2
import imageio
import matplotlib
import numpy as np
import PIL
import scipy
import skimage
import sklearn


def main() -> None:
    image = np.zeros((120, 160), dtype=np.uint8)
    cv2.rectangle(image, (30, 25), (130, 95), 255, -1)
    edges = cv2.Canny(image, 80, 160)

    print("Classic CV environment is ready.")
    print(f"Python packages:")
    print(f"  numpy: {np.__version__}")
    print(f"  opencv: {cv2.__version__}")
    print(f"  scipy: {scipy.__version__}")
    print(f"  scikit-image: {skimage.__version__}")
    print(f"  scikit-learn: {sklearn.__version__}")
    print(f"  pillow: {PIL.__version__}")
    print(f"  imageio: {imageio.__version__}")
    print(f"  matplotlib: {matplotlib.__version__}")
    print(f"Smoke test edge pixels: {int(np.count_nonzero(edges))}")


if __name__ == "__main__":
    main()
