# CPV301 — Computer Vision
## Practical Exam

**Duration:** 90 minutes
**Weight:** 20% of total grade
**Covered LOs:** LO2 → LO9
**Tools allowed:** PyCharm / Jupyter, Python (OpenCV, NumPy, Matplotlib), AI assistant tools (must be used responsibly — see grading criteria)

**Instructions:**
- Answer both questions. Submit your source code, a short report (screenshots + brief explanations), and your **AI Audit Log** (see below) in a single folder.
- You may use AI tools to help write code, but you must be able to explain, adapt, and debug the code yourself. Blind copy-paste without understanding will be penalized under "Conceptual Understanding" and "Critical Thinking".
- Every use of an AI tool during the exam must be recorded in the AI Audit Log. Undisclosed AI usage discovered during grading will be treated as a violation of the AI-assisted skill criterion, not as an academic-integrity case — the goal is transparency, not banning AI.
- All images needed for this exam are provided in the `exam_images/` folder.

---

## Question 1 — Image Denoising (40 points, ~35 minutes)
**Learning Outcomes tested:** LO3 (point operators, linear filtering), with a link to LO4 (edge preservation)

**Provided data:** `exam_images/q1_beach_noise/`
- `my_khe.jpeg` — an aerial photo of Mỹ Khê Beach, Đà Nẵng (clean/original)
- `my_khe_gaussian_noise.jpg` — the same photo with Gaussian noise added
- `my_khe_saltpepper_noise.jpg` — the same photo with salt-and-pepper noise added

**Tasks:**
1. **Noise identification (5 pts):** For each noisy image, identify the type of noise present. Justify your answer (e.g., based on visual appearance and/or pixel intensity histogram).
2. **Denoising (15 pts):** Apply an appropriate filter to remove the noise from each image:
   - Gaussian noise → Gaussian blur (and/or a suitable alternative)
   - Salt-and-pepper noise → Median filter
   Also apply a Bilateral filter to one of the images and compare its edge-preservation behavior to the Gaussian/Median result.
3. **Quantitative evaluation (10 pts):** Compute PSNR and/or SSIM between each denoised image and `my_khe.jpeg`. Present the results in a small table and identify which filter performed best for which noise type.
4. **Discussion (10 pts):** Explain the trade-off between noise removal strength and loss of detail/edges (use a clearly visible edge in the image — e.g., the shoreline, the high-rise buildings, or the tree line — as your example).

---

## Question 2 — Feature Matching and Multi-View Alignment (60 points, ~55 minutes)
**Learning Outcomes tested:** LO4 (feature detection and matching), LO6 (2D/3D feature-based alignment), optional link to LO7 (image stitching)

**Provided data:** `exam_images/q2_bridge_views/`
- `chua_cau_1.jpeg`, `chua_cau_2.jpeg`, `chua_cau_4.jpeg` — the Japanese Covered Bridge (Chùa Cầu), Hội An, shot from roughly the same frontal position but at different times/lighting (daytime, sunset, rainy day)
- `chua_cau_3.jpeg` — an elevated/oblique view of the bridge (shot from a higher vantage point, wider context)
- `chua_cau_5.jpeg` — a side/three-quarter angle view of the bridge

This set intentionally mixes **near-duplicate viewpoints** (1, 2, 4) with **large-baseline viewpoints** (3, 5), so that matching quality will vary sharply across pairs — this is the basis for Task 3.

**Tasks:**
1. **Feature detection & matching (15 pts):** For each pair of images (10 pairs total from 5 images), detect keypoints (SIFT or ORB) and compute feature matches (BFMatcher or FLANN). Visualize the matches for at least one near-duplicate pair (e.g., 1–2) and one large-baseline pair (e.g., 1–3).
2. **Outlier filtering & Homography estimation (15 pts):** Use RANSAC to filter out incorrect matches (outliers) and estimate the Homography matrix for each pair that has enough inliers (state your minimum-inlier threshold and why).
3. **Relative viewpoint analysis (20 pts):** Using the inlier count/ratio from each pair as a similarity measure, build a 5×5 similarity matrix (heatmap) across all images. From it: (a) identify which images share nearly the same viewpoint and which are the most different, (b) explain *why* images 1, 2, 4 are expected to score high similarity despite different lighting, and (c) explain why pairs involving image 3 are expected to score lower.
4. **Bonus — Image stitching (10 pts):** Pick the pair with the highest inlier count, use its homography to warp and blend the two images into a single composite/panorama.

**Note:** Full 3D camera pose recovery (Essential Matrix / triangulation) is *not* required — this task is scoped to 2D feature-based alignment, consistent with course content (Feature Detection & Matching, Feature-based Alignment).

---

## AI Audit Log (Required Submission)

If you use any AI tool (ChatGPT, Claude, Copilot, etc.) at any point during the exam, record every interaction in a table like the one below. Submit it as `ai_audit_log.md` (or `.csv`) alongside your code. If you use no AI at all, submit the file with a single line stating so — an empty/missing log when AI use is evident in your code style will be treated as non-disclosure.

| # | Question | Tool | Prompt (verbatim or summarized) | What the AI returned (brief) | What you changed / verified, and why |
|---|---|---|---|---|---|
| 1 | Q1 | e.g. ChatGPT | "Write Python code to add salt-and-pepper noise to an image with OpenCV" | Gave a function using `np.random.choice` | Fixed a bug where the probability mask was applied to the wrong axis; verified output visually |
| 2 | Q2 | ... | ... | ... | ... |

**What graders look for in the log:**
- Prompts are specific and well-scoped (not just "write code for question 2").
- At least one entry shows you catching and fixing an AI mistake, or adapting generic AI code to this exam's actual files/paths.
- The log is consistent with your submitted code (if the log says you fixed a bug, the fix should be visible in the code).

---

## Grading Rubric (applies to both questions)

| Criterion | Weight | Description |
|---|---|---|
| Correct execution / results | 50% | Code runs without errors and produces expected results (e.g., correctly denoised image, correct homography, correct match visualization) |
| Conceptual understanding | 20% | Student can explain the underlying theory (what noise/filter/homography/RANSAC does and why it's needed) |
| AI-assisted skill | 20% | Judged primarily from the **AI Audit Log**: precise prompts, evidence of detecting/fixing AI errors, evidence of adapting AI output to the actual dataset. A log with only generic prompts and no corrections scores low even if the final code works. |
| Critical thinking | 10% | Student reflects on results — e.g., explains why matching fails between distant viewpoints, why homography degrades with large baseline, or suggests improvements (e.g., pre-smoothing, RANSAC threshold tuning) |
