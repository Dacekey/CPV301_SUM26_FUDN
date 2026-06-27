import cv2
import json
import argparse
from pathlib import Path

points = []

def draw_points(image, pts):
    vis = image.copy()

    # Draw selected points
    for i, (x, y) in enumerate(pts):
        cv2.circle(vis, (x, y), 6, (0, 0, 255), -1)
        cv2.putText(
            vis,
            str(i + 1),
            (x + 8, y - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    # Draw polygon if at least 2 points
    if len(pts) >= 2:
        for i in range(len(pts) - 1):
            cv2.line(vis, pts[i], pts[i + 1], (0, 0, 255), 2)

    # Close polygon if 4 points
    if len(pts) == 4:
        cv2.line(vis, pts[3], pts[0], (0, 0, 255), 2)

    return vis

def mouse_callback(event, x, y, flags, param):
    global points
    original_image, window_name = param

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            print(f"Point {len(points)}: ({x}, {y})")
        else:
            print("Already selected 4 points. Press 'r' to reset or 's' to save.")

    elif event == cv2.EVENT_RBUTTONDOWN:
        if points:
            removed = points.pop()
            print(f"Removed point: {removed}")

    vis = draw_points(original_image, points)
    cv2.imshow(window_name, vis)

def save_points(output_path, pts):
    data = {
        "order": ["top-left", "top-right", "bottom-right", "bottom-left"],
        "points": [{"x": int(x), "y": int(y)} for x, y in pts]
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Saved points to: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Click 4 source points for perspective transform and save coordinates."
    )
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--output", default="selected_points.json", help="Path to output JSON file")
    parser.add_argument("--max_width", type=int, default=1400, help="Resize display if image is too wide")
    args = parser.parse_args()

    image_path = Path(args.image)
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Cannot read image: {image_path}")

    # Optional display resize while preserving coordinate mapping.
    # If image is resized for display, saved coordinates are still in original image coordinates.
    original_h, original_w = image.shape[:2]
    scale = 1.0

    if original_w > args.max_width:
        scale = args.max_width / original_w
        display_w = int(original_w * scale)
        display_h = int(original_h * scale)
        display_image = cv2.resize(image, (display_w, display_h), interpolation=cv2.INTER_AREA)
    else:
        display_image = image.copy()

    display_points = []

    def display_mouse_callback(event, x, y, flags, param):
        global points

        # Convert display coordinate back to original image coordinate
        orig_x = int(round(x / scale))
        orig_y = int(round(y / scale))

        if event == cv2.EVENT_LBUTTONDOWN:
            if len(points) < 4:
                points.append((orig_x, orig_y))
                display_points.append((x, y))
                print(f"Point {len(points)} original: ({orig_x}, {orig_y}) | display: ({x}, {y})")
            else:
                print("Already selected 4 points. Press 'r' to reset or 's' to save.")

        elif event == cv2.EVENT_RBUTTONDOWN:
            if points:
                removed_original = points.pop()
                removed_display = display_points.pop()
                print(f"Removed original point: {removed_original} | display: {removed_display}")

        vis = draw_points(display_image, display_points)
        cv2.imshow(window_name, vis)

    window_name = "Select 4 points: TL -> TR -> BR -> BL"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, display_mouse_callback)

    print("Instructions:")
    print("1. Left click 4 points in this order: top-left, top-right, bottom-right, bottom-left.")
    print("2. Right click to remove the last point.")
    print("3. Press 'r' to reset.")
    print("4. Press 's' to save when 4 points are selected.")
    print("5. Press 'q' or ESC to quit.")

    cv2.imshow(window_name, display_image)

    while True:
        key = cv2.waitKey(20) & 0xFF

        if key == ord("r"):
            points.clear()
            display_points.clear()
            print("Reset all points.")
            cv2.imshow(window_name, display_image)

        elif key == ord("s"):
            if len(points) != 4:
                print(f"Need exactly 4 points. Current: {len(points)}")
            else:
                save_points(args.output, points)

        elif key == ord("q") or key == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
