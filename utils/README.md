# 🛠️ CPV301 Utilities Toolkit (`utils`)

Chào mừng đến với tài liệu hướng dẫn sử dụng thư viện công cụ bổ trợ (`utils`) của dự án Computer Vision (CPV301). Thư viện này được thiết kế theo mô hình **mô-đun hóa (modular)**, cung cấp các hàm tiện ích có tính tái sử dụng cao nhằm tối ưu hóa quy trình phát triển, thực hành trên Jupyter Notebook và xây dựng các pipeline xử lý ảnh.

---

## 📦 Cấu trúc & Danh sách Mô-đun (Module Overview)

Gói `utils` được định hướng là bộ công cụ mở rộng liên tục. Dưới đây là danh sách các mô-đun hiện có và các mô-đun dự kiến trong tương lai:

| Mô-đun | File | Mô tả cốt lõi | Trạng thái |
| :--- | :--- | :--- | :--- |
| **🎨 Visualization** | [`visual.py`](file:///home/dacekey/CPV301_SUM26/utils/visual.py) | Các công cụ hiển thị, so sánh nhiều ảnh song song và vẽ biểu đồ trực quan. | 🟢 Sẵn sàng |
| *📐 Preprocessing* | `preprocess.py` | *Các bộ lọc làm mượt, chuẩn hóa kích thước, cân bằng độ sáng (Histogram Equalization).* | ⏳ *Dự kiến bổ sung* |
| *📊 Metrics* | `metrics.py` | *Các hàm đánh giá chất lượng phân vùng và nhận dạng (IoU, Dice Score, PSNR).* | ⏳ *Dự kiến bổ sung* |
| *🗂️ Data Loader* | `loader.py` | *Hàm đọc tải ảnh hàng loạt, đọc label từ dataset nhanh chóng.* | ⏳ *Dự kiến bổ sung* |

---

## 🚀 Hướng dẫn Import chung (General Usage)

Do các bài thực hành thường nằm bên trong các thư mục con (ví dụ: `main/L16_split_merge_*/L16_main.ipynb`), để gọi được gói `utils`, bạn cần đảm bảo thư mục gốc của dự án đã được thêm vào hệ thống đường dẫn `sys.path`:

```python
import sys
import os

# 1. Thêm đường dẫn gốc của dự án vào sys.path (điều chỉnh số lượng '../' tùy cấp thư mục)
sys.path.append(os.path.abspath("../../")) 

# 2. Import mô-đun hoặc hàm cần sử dụng
from utils.visual import showme
```

---

## 🎨 Chi tiết Mô-đun 1: Visualization ([`visual.py`](file:///home/dacekey/CPV301_SUM26/utils/visual.py))

Mô-đun này chuyên xử lý các nhiệm vụ trực quan hóa dữ liệu hình ảnh trong computer vision, giúp lập trình viên không phải viết lại cấu trúc `matplotlib.pyplot.subplot` lặp đi lặp lại.

### 🔹 Hàm `showme()`

Hàm hỗ trợ hiển thị một danh sách nhiều hình ảnh trên cùng một hàng ngang với tỷ lệ khung hình tự động cân đối và thẩm mỹ.

#### 1. Cú pháp khai báo
```python
def showme(imgs, titles=None, cmap=None, estimate=5)
```

#### 2. Giải thích & Hướng dẫn chỉnh sửa tham số (Parameters)

| Tham số | Kiểu dữ liệu | Giá trị mặc định | Ý nghĩa & Hướng dẫn tinh chỉnh |
| :--- | :--- | :--- | :--- |
| `imgs` | `list` hoặc `tuple` | *(Bắt buộc)* | Danh sách các mảng ảnh (`numpy.ndarray`) cần hiển thị. Ví dụ: `[img1, img2, img3]`. |
| `titles` | `list` của `str` | `None` | Danh sách tiêu đề tương ứng cho từng ảnh. Nếu truyền `None`, ảnh sẽ hiển thị không có tiêu đề phía trên. Nếu truyền, số lượng phần tử nên bằng số lượng ảnh. |
| `cmap` | `str` | `None` | Bảng màu hiển thị (Colormap) của Matplotlib.<br>• **Ảnh màu RGB:** Để mặc định `None`.<br>• **Ảnh nhị phân / Grayscale (1 kênh màu):** Truyền `'gray'` để ảnh không bị ám màu xanh vàng (viridis). |
| `estimate` | `int` hoặc `float` | `5` | Kích thước ước tính (inch) cho chiều rộng và chiều cao của **mỗi** ảnh con.<br>• **Cách hoạt động:** Tổng chiều rộng figure sẽ tự động tính bằng `len(imgs) * estimate`.<br>• **Tinh chỉnh:** Nếu bạn muốn ảnh hiển thị to, rõ nét hơn trên màn hình Jupyter, hãy tăng lên `6` hoặc `8`. Nếu muốn nhỏ gọn để nhìn tổng thể, giảm xuống `3` hoặc `4`. |

#### 3. Yêu cầu đầu vào (Input Requirements)
- **Định dạng không gian màu:** Matplotlib hiển thị ảnh màu theo hệ **RGB**. Nếu bạn đọc ảnh bằng `cv2.imread()` (hệ BGR), bạn **bắt buộc** phải chuyển đổi qua RGB bằng `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` trước khi truyền vào `showme()`.
- **Kích thước ma trận ảnh:** Các ảnh trong list `imgs` không yêu cầu phải có cùng kích thước (chiều rộng/chiều cao). Hàm sẽ tự động sắp xếp vào các ô subplot riêng biệt.

#### 4. Kết quả đầu ra (Output)
- Hàm không trả về biến (`return None`).
- Trực tiếp render và hiển thị một biểu đồ Matplotlib chứa tất cả các ảnh được sắp xếp ngang hàng, tự động ẩn hệ trục tọa độ (`plt.axis("off")`) để khung ảnh sạch sẽ, tập trung vào chi tiết thị giác.

#### 5. Ví dụ minh họa (Code Example)

```python
import cv2
import numpy as np
from utils.visual import showme

# Đọc ảnh từ dataset
img_bgr = cv2.imread("dataset/sample.jpg")
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# Ví dụ 1: Hiển thị 1 ảnh đơn lẻ với kích thước lớn
showme(
    imgs=[img_rgb], 
    titles=["Ảnh gốc RGB (Size lớn)"], 
    estimate=7  # Tăng estimate để phóng to ảnh
)

# Ví dụ 2: So sánh song song ảnh gốc và ảnh Grayscale
showme(
    imgs=[img_rgb, img_gray],
    titles=["Ảnh màu RGB", "Ảnh trắng đen Grayscale"],
    cmap="gray",  # Áp dụng cmap='gray' cho ảnh xám
    estimate=5
)

# Ví dụ 3: Pipeline so sánh nhiều bước xử lý (Thresholding)
_, thresh1 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
_, thresh2 = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

showme(
    imgs=[img_gray, thresh1, thresh2],
    titles=["Grayscale", "Binary Threshold (127)", "Otsu Thresholding"],
    cmap="gray",
    estimate=4  # Giảm estimate xuống 4 vì hiển thị tới 3 ảnh ngang hàng
)
```

---

## 💡 Hướng dẫn Mở rộng cho Lập trình viên (Contribution & Extension Guide)

Thư mục `utils` được thiết kế để dễ dàng mở rộng khi dự án phát triển lớn hơn. Khi bạn muốn bổ sung một tính năng hoặc một mô-đun mới, hãy tuân thủ quy trình 3 bước sau:

1. **Tạo mô-đun chuyên biệt:** Nếu tính năng mới không thuộc mục đích trực quan hóa hình ảnh, **đừng** thêm vào `visual.py`. Hãy tạo một file `.py` mới mang tên mô tả nhóm tính năng đó (ví dụ: `metrics.py` cho tính toán độ chính xác, `preprocess.py` cho lọc nhiễu).
2. **Thiết kế hàm độc lập:** Đảm bảo các hàm tiện ích mới có tính độc lập cao, ít phụ thuộc chéo, luôn đi kèm docstring giải thích tham số rõ ràng.
3. **Cập nhật tài liệu (`README.md`):**
   - Thêm tên file mới vào bảng **Danh sách Mô-đun (Module Overview)** ở mục đầu tiên.
   - Tạo một section mới (ví dụ: `## 📐 Chi tiết Mô-đun 2: Preprocessing`) bên dưới với đầy đủ các mục: *Cú pháp, Bảng giải thích tham số, Yêu cầu đầu vào/ra và Ví dụ code minh họa* tương tự như mô-đun `visual.py` ở trên.
