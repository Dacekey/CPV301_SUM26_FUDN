# AI Audit Log: Le Khoi Nguyen

| # | Question | Tool | Prompt (verbatim or summarized) | What the AI returned (brief) | What you changed / verified, and why |
|---|---|---|---|---|---|
| 1 | Q1-Q2 | ChatGPT/Codex | Create `L30_PE.ipynb` for the practical exam using the provided `CPV301_Practical_Exam.md` and `exam_images`; complete Question 1 and Question 2. | Generated a Jupyter notebook with OpenCV/NumPy/Matplotlib code for denoising, PSNR/SSIM, SIFT feature matching, RANSAC homography, similarity heatmap, and bonus stitching. | Verified actual file paths and image sizes in `main/L30_Practical_Exam_*`; executed the full notebook; confirmed 22 cells ran with 0 errors and saved figures/CSV outputs. |
| 2 | Q1 | ChatGPT/Codex | Choose suitable denoising filters and metrics for Gaussian and salt-and-pepper noise. | Suggested Gaussian blur, median filter, bilateral comparison, and PSNR/SSIM table. | Adjusted Gaussian blur to `3x3, sigma=0.5` after checking PSNR/SSIM; kept median `3x3` for salt-and-pepper because it better preserves structure by SSIM. |
| 3 | Q2 | ChatGPT/Codex | Implement feature matching and homography analysis across all 10 bridge image pairs. | Suggested SIFT with Lowe ratio matching, RANSAC filtering, minimum inlier threshold, heatmap, and simple homography-based stitching. | Tested SIFT settings on the actual bridge images; selected CLAHE + Lowe ratio `0.70`, RANSAC threshold `5 px`, and minimum `8` inliers to make the pairwise matrix stable. |
| 4 | Q1 | ChatGPT/Codex | Asked whether different parameter configurations were tested for Gaussian Blur, Median Filter, and Bilateral Filter, and requested a direct report without changing `L30_PE.ipynb`. | Reported that multiple Q1 filter parameters were tried during preparation: Gaussian kernels/sigmas, median kernel sizes, and bilateral diameter/sigma values. | Did not modify the notebook; inspected saved Q1 metrics and documented that the final notebook kept the selected configurations: Gaussian blur `3x3, sigma=0.5`, median `3x3`, and bilateral `d=9, sigmaColor=75, sigmaSpace=75`. |
| 5 | Q2 | ChatGPT/Codex | Asked to inspect Q2.1/Q2.2 choices, report which SIFT/ORB and BFMatcher/FLANN combinations were implemented or not, explain whether parameter choices were logical, and discuss theoretical effects on Q2.3/Q2.4 without changing the notebook. | Inspected the current notebook and saved Q2 outputs; reported that the executed path uses SIFT + BFMatcher + Lowe ratio + RANSAC homography, with ORB only as fallback and FLANN not implemented. | Did not modify `L30_PE.ipynb`; appended this log entry only. Confirmed executed settings: SIFT, BFMatcher, CLAHE, Lowe ratio `0.70`, RANSAC threshold `5 px`, minimum `8` inliers, and explained expected effects of changing detector/matcher/RANSAC parameters on the similarity matrix and stitching. |

---
# Audit Log Details:

### User's Request #4:
Bay gio hay tra loi giup toi, bat dau voi Q1 truoc, ban da thu chay cac cau hinh khac (parameter) cho cac methods filter nhu Gaussian Blur, Median Filter, Bilateral filter chua? Hay tra loi dua tren task ban da thuc hien, luu y chi tra loi cau hoi, khong duoc chinh sua code trong file notebook main/L30_Practical_Exam_/L30_PE.ipynb hien tai. Vua report truc tiep cho toi vua ghi log bo sung dong moi vao main/L30_Practical_Exam_/NguyenLK_Audit_Log.md theo format table hien tai, luu y khong xoa cac ket qua log truoc do trong markdown audit log nay. Tong hop lai yeu cau: inspect and report, do not change codes in current notebook and write log into Audit log without changing the existing logs.

### AI's Response: (Codex)
Có. Với Q1, trước khi chốt cấu hình trong notebook, tôi đã thử nhiều parameter khác nhau cho các filter:

  - Gaussian Blur: thử kernel 3x3, 5x5, 7x7, 9x9, và thử thêm sigma 0.3, 0.5, 0.8, 1.0, 1.5. Cuối cùng chọn 3x3, sigma=0.5 vì giảm Gaussian noise vừa phải mà không làm mờ cạnh quá
    nhiều. Kết quả final trong notebook: PSNR 26.3674, SSIM 0.6638.

  - Median Filter: thử kernel 3x3, 5x5, 7x7. Cuối cùng chọn 3x3 cho salt-and-pepper noise vì SSIM tốt nhất trong các cấu hình median đã thử và ít làm mất chi tiết hơn kernel lớn. Kết
    quả final: PSNR 22.6643, SSIM 0.7915.

  - Bilateral Filter: thử d=5,7,9, và có thử thêm grid với d=3,5,7,9,11, sigmaColor/sigmaSpace = 25,50,75,100. Cấu hình final trong notebook là d=9, sigmaColor=75, sigmaSpace=75, đạt
    PSNR 28.1294, SSIM 0.8278 trên Gaussian noise. Một vài cấu hình lớn hơn như d=11 có SSIM hơi cao hơn một chút, nhưng PSNR thấp hơn và làm smoothing mạnh hơn, nên tôi giữ d=9 làm
    lựa chọn cân bằng.

  Tôi không chỉnh sửa notebook L30_PE.ipynb. Tôi chỉ append thêm dòng #4 vào NguyenLK_Audit_Log.md theo đúng format table hiện tại.

### User's Request #5:
Nhiem vu tiep theo: kiem tra va bao cao, khong chinh sua code trong notebook hien tai va ghi log vao audit log nhung khong duoc xoa cac lich su log truoc do.
    A. Directory:
    - Notebook: main/L30_Practical_Exam_/L30_PE.ipynb
    - Audit log: main/L30_Practical_Exam_/NguyenLK_Audit_Log.md
    B. Cu the nhiem vu:
    - Yeu cau 1:  O Q2 ban da thuc hien nhung to hop phuong an nao trong Task Q2.1, trong de bai co dua ra lua chon SIFT or ORB, va feature matches nhu BFMatcher or FLANN. Trong notebook ban da thuc hien, ban da thuc hien nhung phuong an nao va chua thuc hien cai nao va neu da thu cac to hop roi thi co ban so sanh phuong an tot nhat chua?
    - Yeu cau 2: O Q2, task Q2.2, giai thich cho toi vi sao ban chon cac lua chon cau hinh tham so do va phuong an ban da thuc thi de den duoc ket qua cuoi cung do, confirm voi toi rang ban da co mot trinh tu suy luan logic chat che va logic de den ket qua do hay chi la mot su cau hinh tham so mot cach ngau nhien.
    - Yeu cau 3: nhu trong luu y o tren, ban khong duoc chinh sua code. Hay thu gia dinh neu thay doi mot vai cau hinh tham so o 2 yeu cau tren thi ket qua trong task Q2.3 va Q2.4 se thay doi nhu the nao ve mat ly thuyet.

### AI's Response: (Codex)
• Đã kiểm tra và không chỉnh sửa code trong L30_PE.ipynb. Tôi chỉ append thêm dòng #5 vào NguyenLK_Audit_Log.md.

  Yêu Cầu 1

  Trong notebook hiện tại, Q2.1 đã thực thi:

  - Detector: SIFT
  - Matcher: BFMatcher
  - Descriptor norm: cv2.NORM_L2
  - Matching strategy: KNN matching + Lowe ratio test
  - Executed config: Detector: SIFT, Lowe ratio: 0.70

  Các phương án chưa thực thi trong notebook:

  - ORB: có code fallback nếu máy không có SIFT, nhưng môi trường này có SIFT nên ORB không được chạy.
  - FLANN: không được implement/chạy trong notebook.
  - Không có bảng benchmark đầy đủ kiểu SIFT+BF, SIFT+FLANN, ORB+BF, ORB+FLANN.

  Tôi có thử tuning trước khi chốt notebook, nhưng chủ yếu trên pipeline SIFT + BFMatcher, gồm các biến thể như grayscale thường, CLAHE, resize, và Lowe ratio 0.70 / 0.75 / 0.80. Vì
  vậy: có so sánh cấu hình trong pipeline SIFT+BF, nhưng chưa so sánh toàn bộ tổ hợp SIFT/ORB x BF/FLANN.

  Yêu Cầu 2

  Cấu hình Q2.2 không chọn ngẫu nhiên. Trình tự logic là:

  - Dùng SIFT vì ảnh có thay đổi lighting/viewpoint; SIFT ổn hơn ORB cho scale, rotation và illumination changes.
  - Dùng CLAHE trước feature extraction để giảm khác biệt ánh sáng giữa daytime/sunset/rainy images.
  - Dùng BFMatcher vì dataset chỉ có 5 ảnh, số descriptor không quá lớn; BF exact matching đủ ổn định, FLANN chủ yếu có lợi hơn về tốc độ khi dataset lớn.
  - Chọn Lowe ratio 0.70 vì stricter hơn 0.75/0.80, giúp giảm false matches ở large-baseline pairs.
  - Chọn RANSAC threshold 5 px để cho phép sai số định vị keypoint nhỏ nhưng vẫn loại outlier lớn.
  - Chọn minimum inliers = 8 vì homography chỉ cần 4 điểm về mặt toán học, nhưng 4 là quá yếu; 8 là ngưỡng an toàn hơn để xem homography là đáng tin.

  Kết quả cuối hiện tại: pair mạnh nhất là 1-5 với 27 inliers, sau đó 2-5 với 18, 1-2 với 16; pair 1-3 yếu nhất với 0 inliers.

  Yêu Cầu 3

  Nếu thay đổi cấu hình, về lý thuyết Q2.3 và Q2.4 sẽ đổi như sau:

  - Nếu dùng ORB thay SIFT: khả năng cao inlier counts giảm và matrix Q2.3 nhiễu hơn, nhất là các cặp khác lighting/viewpoint. Stitching Q2.4 có thể kém ổn định hơn.
  - Nếu dùng FLANN thay BFMatcher với SIFT: kết quả có thể gần tương đương nếu FLANN params đúng, nhưng có thể hơi khác match ordering/inlier count. Lợi ích chính là tốc độ, không phải
    chất lượng trên dataset nhỏ này.

  - Nếu tăng Lowe ratio lên 0.75 hoặc 0.80: sẽ có nhiều good matches hơn, nhưng nhiều outliers hơn; RANSAC có thể tăng inlier count ở vài cặp nhưng inlier ratio giảm, heatmap dễ
    overestimate similarity.

  - Nếu giảm Lowe ratio xuống 0.60/0.65: matches sạch hơn nhưng ít hơn; nhiều pair có thể không đủ inliers, heatmap thưa hơn, stitching có thể fail nếu pair tốt cũng mất quá nhiều
    matches.

  - Nếu giảm RANSAC threshold xuống 3 px: inliers giảm, matrix Q2.3 chặt hơn; stitching chỉ tốt nếu vẫn còn đủ inliers.
  - Nếu tăng RANSAC threshold lên 8-10 px: inliers tăng giả tạo, nhưng dễ giữ outliers; Q2.3 có thể nhìn “đẹp” hơn nhưng Q2.4 dễ bị warp sai/ghosting.
  - Nếu tăng MIN_INLIERS lên 15/20: ít pair được xem là homography valid hơn; Q2.4 gần như chỉ còn các pair mạnh như 1-5, 2-5, 1-2.
  - Nếu giảm MIN_INLIERS xuống 4: nhiều homography yếu sẽ được chấp nhận, nhưng dễ sai về mặt hình học, đặc biệt các pair liên quan image 3.

  Tóm lại: kết quả hiện tại đến từ một pipeline có lý do rõ ràng, không phải cấu hình ngẫu nhiên.