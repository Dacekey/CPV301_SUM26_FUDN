# CPV301 — Lab 4

**Learning Outcome tested:** LO9 — Explain the principles of face recognition, object tracking
**Tools allowed:** PyCharm / Jupyter, Python (OpenCV, and a face-embedding library such as `face_recognition` / `dlib` / OpenCV DNN face module), AI assistant tools

**Instructions:**
- Submit your source code, a short report (screenshots + brief explanations).
- All images needed are provided in `exam_images/q_lab4_faces/` (see "Provided data" below).

---

## Provided data
All photos are official U.S. government portraits (public domain, `PD-USGov`), sourced from Wikimedia Commons.

**Gallery / enrollment photos** — `exam_images/q_lab4_faces/gallery/`
- `obama_2009.jpg` — official portrait of Barack Obama, Jan. 13, 2009
- `gwbush.jpg` — official portrait of George W. Bush

**Query photos** — `exam_images/q_lab4_faces/query/`
- `obama_2013_query.jpg` — Barack Obama, different sitting, Dec. 6, 2012 (same person as gallery, 4 years later, different lighting/studio) → students should recognize this as a **match**
- `ghwbush_unknown.jpg` — George H. W. Bush (father of George W. Bush; visually similar but a different identity, not in the gallery) → students should recognize this as **Unknown** — a deliberately hard negative, useful for the Task 4 discussion on look-alikes

---

## Tasks

1. **Face detection (10 pts)**
   Detect all faces in each gallery photo and each query photo (e.g., Haar cascade, HOG, or a DNN face detector). Draw bounding boxes and report how many faces were found in each image.

2. **Face embedding & comparison (20 pts)**
   For each detected face, compute a face embedding/descriptor. Compute the distance (e.g., Euclidean or cosine) between each query face and every gallery face.

3. **Recognition decision (10 pts)**
   Choose a distance threshold and decide, for each query face, whether it matches a known identity or should be labeled "Unknown." State the threshold you chose and why.

4. **Discussion (10 pts)**
   Explain at least two realistic causes of a wrong decision in this pipeline (e.g., poor lighting, extreme pose/angle, occlusion (glasses/mask), low resolution, look-alikes/twins) and how each could be mitigated.

**Total: 50 pts**

## Grading Rubric
| Criterion | Weight | Description |
|---|---|---|
| Correct execution / results | 70% | Face detection and matching code runs and produces correct results on the provided data |
| Conceptual understanding | 30% | Can explain what a face embedding is and why distance/threshold-based matching works |

---
