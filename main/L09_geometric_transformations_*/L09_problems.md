# Thiết Kế Bài Thực Hành: Geometric Transformations (UAV-CV)

> [!NOTE]
> **Định hướng thiết kế:** Bài thực hành được xây dựng theo hướng *"vừa bám sát lý thuyết Geometric Transformations, vừa mang tính ứng dụng thực tế trong UAV-CV"*. Bài lab phân định rõ những thao tác có thể thực hiện trên Notebook đơn giản và những giới hạn thực tế khi xây dựng Orthophoto/Orthomosaic chuẩn.

---

## 📋 Tổng quan Đề xuất

Đề xuất chia thành **2 bài thực hành chính**:
1. **Bài 1:** Perspective Transform / Bird-eye View từ ảnh UAV nghiêng.
2. **Bài 2:** Mô phỏng Orthophoto đơn giản từ ảnh UAV & So sánh giới hạn với Orthomosaic thật.

### Lý do tách thành 2 bài:
Mặc dù Bài 2 có bao gồm tư tưởng của Bài 1 (vì Orthophoto cũng cần chỉnh camera tilt / perspective), nhưng phạm vi của Bài 2 rộng hơn rất nhiều. Một Orthophoto đúng nghĩa còn liên quan đến:
- **Lens distortion** (biến dạng ống kính)
- **Thông số camera** (Camera calibration & pose)
- **Tọa độ địa lý** (GPS/IMU, Georeferencing)
- **Mô hình độ cao địa hình** (DEM/DSM) để sửa topographic relief
- **Ghép nối nhiều ảnh** (Mosaic blending, Bundle adjustment)

👉 **Phân bổ mục tiêu:**
- **Bài 1:** Nắm chắc bản chất toán học & lập trình của **Perspective Transform** bằng 4 điểm.
- **Bài 2:** Nâng cấp tư duy sang **UAV Mapping**: Từ xử lý ảnh nghiêng $\rightarrow$ ảnh mô phỏng Orthophoto $\rightarrow$ hiểu rõ giới hạn kỹ thuật.

---

## 🛠 BÀI 1: Perspective Transform — Từ ảnh UAV nghiêng sang Bird-eye View

### 1. Mục tiêu
Biến một ảnh chụp nghiêng/méo thành ảnh nhìn thẳng từ trên xuống (*Bird-eye view*) thông qua biến đổi **Perspective Transform / Homography**.

> **Liên hệ bài học:** Bám sát nội dung *Geometric Transformations, Inverse Warping,* và *Resampling*. Quá trình warping/resampling tính toán lại giá trị pixel mới; trong đó **Inverse Warping** được sử dụng để tránh hiện tượng rỗng lỗ (*holes/cracks*) trên ảnh đích.

### 2. Dữ liệu đầu vào (Input)
Một ảnh UAV hoặc ảnh mô phỏng có **mặt phẳng rõ ràng**, ví dụ:
- Sân bóng, bãi đỗ xe, mặt đường
- Ruộng đồng hình chữ nhật, mái nhà phẳng
- *(Hoặc để test mẫu:* Tờ giấy / biển báo chụp nghiêng)

💡 *Yêu cầu:* Ảnh nên có một vùng ngoài đời thực là hình chữ nhật, nhưng do góc chụp bị biến dạng thành hình thang trong ảnh.

### 3. Ý tưởng thuật toán
1. **Xác định 4 điểm nguồn (Source points):** Chọn 4 góc của vùng mặt phẳng cần chỉnh trên ảnh gốc theo thứ tự:
   - `Top-Left` (Trên - Trái)
   - `Top-Right` (Trên - Phải)
   - `Bottom-Right` (Dưới - Phải)
   - `Bottom-Left` (Dưới - Trái)
2. **Định nghĩa 4 điểm đích (Destination points):** Là 4 góc của một hình chữ nhật chuẩn kích thước $W \times H$:
   - $(0, 0)$
   - $(W, 0)$
   - $(W, H)$
   - $(0, H)$
3. **Tính ma trận biến đổi:** Tính ma trận Homography / Perspective $M$ (kích thước $3 \times 3$).
4. **Warp ảnh:** Áp dụng biến đổi để thu được ảnh góc nhìn từ trên xuống.

### 4. Pipeline thực hành
1. Đọc và hiển thị ảnh gốc.
2. Chọn 4 điểm source trên ảnh nghiêng (hardcode tọa độ hoặc click chuột tương tác).
3. Định nghĩa 4 điểm destination dạng hình chữ nhật.
4. Tính ma trận biến đổi perspective (`cv2.getPerspectiveTransform`).
5. Dùng `cv2.warpPerspective` để tạo ảnh bird-eye view.
6. So sánh ảnh gốc và ảnh sau khi chỉnh sửa.
7. **Thử nghiệm & so sánh các phương pháp Interpolation (Resampling):**
   - `INTER_NEAREST` (Nearest Neighbor)
   - `INTER_LINEAR` (Bilinear Interpolation - mặc định)
   - `INTER_CUBIC` (Bicubic Interpolation)
   - `INTER_AREA` (Dùng khi thu nhỏ / downsample ảnh)
8. Nhận xét hiện tượng mờ (blur), răng cưa, aliasing.

### 5. Kiến thức rút ra (Ghi nhớ trong Notebook)
- **Perspective transform** là một phép biến đổi hình học (*image warping*) mạnh mẽ cho các mặt phẳng 2D trong không gian 3D.
- Trong **UAV-CV**, kỹ thuật này giúp đưa ảnh mặt đất từ góc chụp nghiêng về góc nhìn thẳng từ trên xuống (*bird-eye view*).
- Sau biến đổi, tọa độ pixel đích thường là số thực, không rơi vào lưới pixel nguyên, do đó bắt buộc phải có bước **Interpolation / Resampling**.

### 6. Câu hỏi phân tích
1. Vì sao bắt buộc phải chọn tối thiểu 4 điểm không thẳng hàng để tính ma trận Perspective?
2. Nếu chọn tọa độ 4 điểm nguồn bị sai/lệch, ảnh kết quả sẽ gặp hiện tượng gì?
3. Perspective transform có thể sửa được biến dạng do địa hình đồi núi cao thấp không? Vì sao?
4. Giải thích nguyên nhân ảnh sau khi warp có thể bị blur hoặc xuất hiện răng cưa (*aliasing*).
5. Khi nào nên ưu tiên dùng `INTER_AREA`, `INTER_LINEAR`, hay `INTER_CUBIC`?

---

## 🛰 BÀI 2: Mô phỏng Orthophoto đơn giản từ ảnh UAV

**Links:** https://youtu.be/g8mapLUXyGI?si=L8Qc6LZvG9dd0Nqe
(Watch this video for understand **Orthomosaic**)

### 1. Mục tiêu
Thực hiện một quy trình "gần với Orthophoto" nhưng phù hợp với quy mô bài lab: Sử dụng một ảnh UAV chụp nghiêng, chỉnh về góc nhìn top-down và phân tích nguyên nhân vì sao đây chỉ là **Orthophoto đơn giản / mô phỏng (Approximation)** chứ chưa phải Orthophoto chuẩn.

> [!WARNING]
> **Vì sao không làm Orthomosaic thật ngay trên một ảnh?**
> Một Orthomosaic chuẩn trong thực tế đòi hỏi sự kết hợp phức tạp của:
> - Nhiều ảnh UAV chụp chồng lấn (*overlap*)
> - Camera calibration & tham số lens distortion
> - Camera pose / GPS / IMU
> - Dữ liệu địa hình DEM/DSM để sửa topographic relief (*độ lệch do địa hình*)
> - Image matching, Bundle adjustment, Orthorectification, Mosaic blending & Georeferencing
> 
> *Do đó, nếu chỉ dùng 1 ảnh đơn, ta không thể sửa chính xác topographic relief.* Tên gọi phù hợp cho bài này là **Simple Orthophoto-like Rectification** hoặc **Single-image Orthorectification Approximation**.

### 2. Dữ liệu đầu vào (Input)
Một ảnh UAV chụp nghiêng với khu vực mặt đất **tương đối bằng phẳng**.
- **Ví dụ tốt:** Bãi đỗ xe, sân trường, cánh đồng phẳng, đoạn đường thẳng, khu đất trống.
- **Tránh:** Địa hình đồi núi phức tạp, khu vực có thung lũng sâu (vì thiếu DEM/DSM để nắn chỉnh).

### 3. Ý tưởng các mức độ xử lý
Quy trình được chia thành 4 mức độ (Levels):
- **Mức 1 (Khử méo):** Sửa lỗi lens distortion (nếu có thông số calibration).
- **Mức 2 (Nắn phối cảnh):** Sửa camera tilt / perspective bằng Homography.
- **Mức 3 (Định tỷ lệ):** Resize / scale ảnh về một tỷ lệ kích thước gần với bản đồ.
- **Mức 4 (Phân tích lỗi):** Đánh giá các phần chưa sửa được (*topographic relief, chiều cao công trình/cây cối, địa hình 3D*).

*(Lưu ý: Nếu chưa có calibration matrix, có thể bỏ qua bước 1 hoặc mô phỏng bằng ảnh tự tạo distortion).*

### 4. Pipeline thực hành
1. Đọc và hiển thị ảnh UAV gốc.
2. **Khử méo ống kính (Tùy chọn):**
   - Nếu có thông số: Dùng `cv2.undistort` với Camera Matrix & Distortion Coefficients.
   - Nếu không có: Bỏ qua hoặc dùng ảnh mô phỏng.
3. Chọn vùng mặt đất phẳng cần nắn chỉnh (*orthorectify*).
4. Áp dụng Perspective Transform để đưa vùng mặt đất đó về góc nhìn thẳng từ trên xuống (*top-down view*).
5. Resize kết quả về một kích thước hoặc tỷ lệ (*scale*) cố định.
6. **So sánh trực quan:** Ảnh gốc $\rightarrow$ Ảnh sau undistort $\rightarrow$ Ảnh sau perspective transform.
7. **Phân tích sai số thực tế:** Đánh dấu (*khoanh vùng*) các chi tiết bị lệch hình học:
   - Cây cao, nhà cao tầng (*hiện tượng xô nghiêng / leaning*)
   - Đồi dốc, địa hình gồ ghề
   - Các vật thể nằm ngoài mặt phẳng chuẩn
8. Viết nhận xét tổng kết lý do vì sao ảnh kết quả chưa thể thay thế bản đồ Orthophoto chuẩn.

### 5. Kiến thức rút ra (Ghi nhớ trong Notebook)
- **Orthophoto** là ảnh bản đồ đã được nắn chỉnh vuông góc, loại bỏ độ nghiêng camera và độ lệch địa hình, đảm bảo tỷ lệ khoảng cách đồng nhất ở mọi điểm.
- Với 1 ảnh đơn và giả định mặt đất phẳng lý tưởng, ta có thể tạo ra ảnh xấp xỉ Orthophoto bằng Perspective Transform.
- Vật thể có chiều cao (3D) nằm trên mặt phẳng đó sẽ bị hiện tượng xô hình (*relief displacement*) không thể khắc phục chỉ bằng 2D homography.
- **Orthomosaic** là quá trình ghép nối hàng loạt ảnh orthophoto để tạo thành bản đồ quy mô lớn.

### 6. Câu hỏi phân tích
1. Vì sao kết quả của bài thực hành này chưa thể gọi là Orthomosaic chuẩn?
2. Tại sao một ảnh đơn không chứa đủ thông tin để sửa lỗi topographic relief (*sai lệch độ cao địa hình*)?
3. Giải thích hiện tượng các vật thể cao (*nhà, cây*) bị đổ nghiêng về phía rìa ảnh sau khi biến đổi perspective.
4. Phép biến đổi Perspective Transform dựa trên giả định căn bản nào về không gian?
5. Để xây dựng một hệ thống tạo Orthomosaic hoàn chỉnh trong thực tế, hệ thống UAV cần thu thập những loại dữ liệu nào?

---

## 💡 BÀI THAY THẾ (TÙY CHỌN): Mini Orthomosaic từ 2–4 ảnh UAV chồng lấn

> [!TIP]
> Nếu muốn Bài 2 mang tính chất ghép ảnh thực tế hơn (*stitching*) và không đi quá sâu vào lý thuyết trắc địa/DEM, bạn có thể thay thế bằng bài **Mini Orthomosaic**:

### Quy trình thực hiện:
1. Chuẩn bị 2–4 ảnh UAV có độ chồng lấn (*overlap từ 30% - 60%*).
2. Phát hiện đặc trưng điểm (*Feature Detection*) sử dụng **SIFT** hoặc **ORB**.
3. Khớp đặc trưng (*Feature Matching*) giữa các cặp ảnh.
4. Ước lượng ma trận Homography bằng thuật toán **RANSAC** để loại bỏ nhiễu (*outliers*).
5. Warp các ảnh về cùng một hệ tọa độ mặt phẳng.
6. Pha trộn màu sắc (*Blending / Seam blending*) để tạo thành một ảnh mosaic nhỏ hoàn chỉnh.

*👉 **Đánh giá:** Bài này rèn luyện rất tốt các kỹ thuật Feature Matching, RANSAC, và Warping trong CV, nhưng sẽ không tập trung vào khái niệm Topographic relief / Orthophoto.*

---

## 📑 Đề xuất Cấu trúc Notebook (`.ipynb`)

Để sinh viên/người học dễ theo dõi nhất, Notebook thực hành nên được tổ chức theo bố cục sau:

```text
Lab: Geometric Transformations for UAV-CV

│
├── Part 1: Perspective Transform for Bird-eye View
│   ├── 1.1 Objective & Theory
│   ├── 1.2 Load & Visualize Image
│   ├── 1.3 Select Source & Destination Points
│   ├── 1.4 Compute Homography & Warp Image
│   ├── 1.5 Compare Interpolation Methods (Nearest, Linear, Cubic, Area)
│   └── 1.6 Discussion & Analysis Questions
│
└── Part 2: Single-image Orthophoto Approximation
    ├── 2.1 Objective: What is an Orthophoto?
    ├── 2.2 Load UAV Image & (Optional) Lens Undistortion
    ├── 2.3 Correct Camera Tilt using Homography
    ├── 2.4 Error Analysis: Relief Displacement & Limitations
    ├── 2.5 Why this is NOT a full Orthomosaic?
    └── 2.6 Real-world Requirements for UAV Mapping
```

### 🎯 Lời kết
- **Bài 1** là nền tảng kỹ thuật toán học & lập trình ảnh.
- **Bài 2** là tư duy ứng dụng thực tế trong UAV Mapping, giúp người học hiểu rõ ranh giới giữa xử lý ảnh 2D đơn thuần và xử lý đo đạc không gian (*Photogrammetry*).

### Note from Author:
Because Problem 2 needs more techniques to implement, so it's over this lab's limit. The core technique of this problem is quite the same to Problem 1.