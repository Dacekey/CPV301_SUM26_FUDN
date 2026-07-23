# BÀI THỰC HÀNH: TỰ ĐỘNG NHẬN DIỆN VÀ GHÉP ẢNH TOÀN CẢNH (AUTOMATED PANORAMA RECOGNITION AND STITCHING)

## PHẦN 1: CƠ SỞ LÝ THUYẾT

### 1. Đặt vấn đề: Tại sao cần "Nhận diện" Panorama?
Trong các bài toán ghép ảnh thông thường, người dùng thường chụp ảnh theo một thứ tự tuần tự nhất định (ví dụ: từ trái sang phải, từ trên xuống dưới). Khi đó, việc xác định thứ tự ghép ảnh rất đơn giản. 

Tuy nhiên, trong thực tế, các tập dữ liệu ảnh thu thập được thường ở dạng **lộn xộn (unordered image collections)**. Người chụp có thể nhảy cóc góc chụp, chụp thành nhiều tầng (multi-row panorama), hoặc chụp vòng tròn khép kín $360^\circ$ nơi ảnh đầu và ảnh cuối phải khớp với nhau. Do đó, hệ thống cần phải có khả năng tự động nhận diện bức ảnh nào thuộc về cùng một khung cảnh và chúng có vùng chồng lấn (overlap) với những bức ảnh nào khác để tiến hành lắp ghép mà không cần sự can thiệp thủ công từ con người.

### 2. Quy trình nhận diện ảnh Panorama tổng quát
Quy trình này biến một tập hợp ảnh đầu vào lộn xộn thành các bức ảnh toàn cảnh hoàn chỉnh thông qua hai giai đoạn lớn:

#### Giai đoạn 1: Tìm các vùng chồng lấn theo từng cặp (Pairwise Overlaps)
* **Trích xuất đặc trưng (Feature Extraction):** Sử dụng các thuật toán trích xuất điểm đặc trưng bất biến với tỉ lệ và góc quay (như SIFT). Các vị trí điểm đặc trưng và bộ mô tả (feature descriptors) của **tất cả** các ảnh đầu vào sẽ được trích xuất và lưu trữ vào một cấu trúc dữ liệu chỉ mục (indexing structure) như KD-Tree để tối ưu hóa tốc độ tìm kiếm.
* **Khớp điểm đặc trưng (Feature Matching):** Với mỗi điểm đặc trưng trong một bức ảnh, hệ thống sử dụng cấu trúc chỉ mục để tìm nhanh các ứng viên tiềm năng gần nhất (Nearest Neighbors) trên các bức ảnh khác dựa trên khoảng cách của bộ mô tả. Từ đó, thiết lập các cặp ảnh có mối quan hệ chồng lấn ban đầu.

#### Giai đoạn 2: Gom cụm thành phần liên thông (Connected Components)
* Hệ thống mô hình hóa tập dữ liệu dưới dạng một **Đồ thị (Graph)**: Trong đó mỗi bức ảnh là một **đỉnh (node)**, và mỗi quan hệ khớp nhau hợp lệ giữa hai bức ảnh là một **cạnh (edge)**.
* Thuật toán sẽ duyệt đồ thị để tìm các **thành phần liên thông (connected components)**. Mỗi thành phần liên thông đại diện cho một nhóm các bức ảnh thuộc về cùng một khung cảnh panorama độc lập.
* Cuối cùng, từng nhóm này sẽ được đưa vào bộ căn chỉnh tọa độ toàn cục (Global Registration/Bundle Adjustment) và tiến hành hòa trộn (Blending) thành ảnh panorama hoàn chỉnh.

### 3. Thách thức lớn nhất trong Nhận diện Panorama
* **Cấu trúc lặp đi lặp lại (Repeated Structures):** Các chi tiết giống hệt nhau xuất hiện nhiều lần trong cảnh (ví dụ: các ô cửa sổ giống nhau trên một tòa nhà, các họa tiết gạch) dễ đánh lừa bộ mô tả đặc trưng, dẫn đến việc kết nối sai các bức ảnh không liên quan (False Matches).
* **Giải pháp truyền thống (Không dùng ML/DL):** Để loại bỏ các kết nối sai này, thuật toán thường áp dụng phương pháp so sánh trực tiếp sai số pixel (direct pixel error comparison) giữa các vùng đã được căn chỉnh để xác thực xem chúng có thực sự là cùng một cảnh hay không. Tuy nhiên, phương pháp này có thể bị ảnh hưởng nếu cảnh có chứa các vật thể chuyển động (như người đi bộ, xe cộ) gây ra sự bất nhất về mặt quang học.

---

## PHẦN 2: HƯỚNG DẪN THỰC HÀNH

### 1. Mô tả bài thực hành
Mục tiêu của bài thực hành là xây dựng một đường ống (pipeline) xử lý bằng ngôn ngữ lập trình (ví dụ: Python kết hợp OpenCV) để nhận diện và ghép các bức ảnh toàn cảnh từ một thư mục chứa ảnh bị xáo trộn thứ tự đầu vào. 

Bạn sẽ chuẩn bị một tập dữ liệu gồm từ 10 - 15 bức ảnh bị xáo trộn tên file, trong đó bao gồm:
* Một nhóm khoảng 6-8 ảnh chụp một khung cảnh panorama (có vùng chồng lấn).
* Một vài bức ảnh "nhiễu" khác hoàn toàn (không liên quan đến khung cảnh trên) để kiểm tra khả năng phân loại và gom cụm của thuật toán.

### 2. Kết quả đầu ra mong đợi (Expected Outputs)
* **Đồ thị liên thông:** Một sơ đồ hiển thị mối quan hệ giữa các ảnh (Ví dụ: Ảnh 1 nối với Ảnh 3, Ảnh 3 nối với Ảnh 2; Ảnh 5 và Ảnh 6 đứng cô lập...).
* **Danh sách Panorama được nhận diện:** Output dạng text hiển thị rõ hệ thống tìm ra bao nhiêu nhóm ảnh toàn cảnh (Connected Components). *Ví dụ: Group 1: [img3.jpg, img1.jpg, img2.jpg]. Group 2 (Nhiễu): [img4.jpg].*
* **Ảnh Panorama hoàn chỉnh:** Bức ảnh composite cuối cùng được ghép khít từ nhóm ảnh hợp lệ, các ảnh nhiễu phải bị loại bỏ hoàn toàn.

### 3. Giải pháp về thuật toán và các kỹ thuật sử dụng

Để triển khai bài toán này mà không sử dụng Học máy (ML) hay Học sâu (DL), bạn có thể sử dụng các thuật toán và cấu trúc hình học cổ điển sau:

#### Bước 1: Phát hiện điểm đặc trưng và Tạo bộ mô tả
* **Kỹ thuật đề xuất:** Sử dụng thuật toán **SIFT (Scale-Invariant Feature Transform)** hoặc **SURF / ORB**. SIFT được khuyến khích vì có độ chính xác cao, bất biến với các phép xoay, thu phóng và thay đổi độ sáng nhẹ khi bạn xoay camera.

#### Bước 2: Khớp đặc trưng theo cặp và Loại bỏ nhiễu hình học
* **Kỹ thuật đề xuất:** Sử dụng bộ khớp **Brute-Force Matcher** hoặc **FlannBasedMatcher** (sử dụng cấu trúc cây KD-Tree để khớp nhanh hơn).
* **Kỹ thuật lọc điểm khớp sai (Ratio Test):** Áp dụng **Lowe's Ratio Test** (giữ lại các điểm khớp có tỉ lệ khoảng cách giữa điểm gần nhất và điểm gần thứ hai nhỏ hơn một ngưỡng cố định, ví dụ 0.7 hoặc 0.8) để loại bỏ phần lớn các điểm khớp sai ban đầu.
* **Xác thực hình học với RANSAC:** Dù đã lọc qua Ratio Test, các điểm khớp vẫn có thể sai do cấu trúc lặp lại. Bạn cần sử dụng thuật toán **RANSAC (Random Sample Consensus)** để ước lượng ma trận **Homography ($H$)** giữa từng cặp ảnh. RANSAC sẽ tìm ra tập hợp các điểm khớp đồng thuận về mặt hình học phẳng (inliers) và loại bỏ các điểm khớp sai lệch hoàn toàn (outliers). Nếu số lượng cặp điểm inliers giữa hai ảnh vượt quá một ngưỡng nhất định (ví dụ: > 40 điểm), cặp ảnh đó mới được coi là có kết nối hợp lệ.

#### Bước 3: Xây dựng Đồ thị và Gom cụm nhóm ảnh
* **Kỹ thuật đề xuất:** Sử dụng thuật toán tìm kiếm theo chiều rộng **BFS (Breadth-First Search)** hoặc tìm kiếm theo chiều sâu **DFS (Depth-First Search)** để duyệt đồ thị.
* Coi mỗi ảnh là một nút. Nếu bước 2 xác định hai ảnh có ma trận Homography hợp lệ, hãy thêm một cạnh nối giữa chúng. Duyệt BFS/DFS sẽ giúp bạn tìm ra tất cả các thành phần liên thông (Connected Components) - chính là các nhóm ảnh thuộc về cùng một bức panorama.

#### Bước 4: Căn chỉnh hình ảnh toàn cục (Alignment)
* **Kỹ thuật đề xuất:** Chọn một bức ảnh nằm ở trung tâm của nhóm làm ảnh gốc (Reference Image) để cố định hệ tọa độ. Sử dụng các ma trận Homography đã tính được ở Bước 2 để thiết lập chuỗi biến đổi hình học đưa tất cả các ảnh khác trong nhóm về chung hệ mặt phẳng của ảnh gốc.
* *(Nâng cao nếu có hiện tượng tích tụ sai số drift):* Áp dụng thuật toán tối ưu hóa **Bundle Adjustment** để tinh chỉnh đồng thời các tham số ma trận xoay của các camera.

#### Bước 5: Hòa trộn hình ảnh (Blending)
* **Kỹ thuật đề xuất:** Sau khi biến đổi (warp) các ảnh về chung một mặt phẳng, tại các vùng chồng lấn sẽ xuất hiện lỗi ranh giới rõ rệt (seams) do sự khác biệt về độ sáng. Hãy sử dụng kỹ thuật **Feathering (Alpha Blending)** hoặc nâng cao hơn là **Multi-band Blending (Pyramid Blending)** để làm mờ các đường ranh giới, giúp bức ảnh panorama đầu ra mượt mà và tự nhiên nhất.
