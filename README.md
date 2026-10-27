Dưới đây là nội dung file `README.md` đã được chỉnh sửa đúng ý thầy. Bạn có thể bôi đen và copy trực tiếp đoạn văn bản bên dưới (không có code block) để dán đè vào file của bạn nhé:

# 🎯 Chinh Hop Visualizer App (DT035)

> **Đồ án môn học Cấu trúc Dữ liệu và Giải thuật (INT13185)**  
> Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
> Được thiết kế và mở rộng thành ứng dụng Web trực quan hóa thuật toán (Algorithm Visualizer) chuẩn production.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-brightgreen)](https://chinh-hop-app.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

---

## 📑 THÔNG TIN ĐỒ ÁN & HƯỚNG DẪN ĐỐI CHIẾU (Theo Rubric)

### 1. Nhận diện

- **Họ và tên:** Vũ Duy Khánh
- **MSSV:** N24DCDT039
- **Lớp:** D24CQDT01-N
- **Mã đề:** DT035
- **Tên đề:** Liệt kê chỉnh hợp không lặp chập k của n phần tử
- **Đường dẫn phiếu:** `05_Minh_chung_cu_the_91_de_tai.docx` (Mục DT035)
- **Căn cứ giáo trình:** Chương 3, Bài tập chương 3, câu 22; vận dụng mục 3.2 (Thuật toán sinh kế tiếp) và 3.3 (Liệt kê bằng đệ quy); trang in 64, 71–72, 86; trang PDF 76, 83–84, 98.

### 2. Môi trường

- **Ngôn ngữ:** Python 3.11
- **Thư viện sử dụng:** `Flask==3.0.0` (Web Server), `pytest==7.4.0` (Kiểm thử), `gunicorn==21.2.0` (Triển khai). Thuật toán lõi không sử dụng thư viện ngoài.
- **Lệnh cài đặt:** `pip install -r requirements.txt`

### 3. Lệnh

- **Chạy Ví dụ 1 (n=3, k=2):**
  `python -c "from logic import liet_ke_chinh_hop; print(liet_ke_chinh_hop(3, 2))"`
- **Chạy Ví dụ 2 (n=2, k=2):**
  `python -c "from logic import liet_ke_chinh_hop; print(liet_ke_chinh_hop(2, 2))"`
- **Lệnh nhập dữ liệu mới (Giao diện Web):**
  `python app.py` (Truy cập `http://localhost:5000`).
- **Lệnh chạy toàn bộ kiểm thử (hiển thị chi tiết):**
  `pytest tests/test_logic.py -v -s`
- **Lệnh chạy đo đạc hiệu năng (Benchmark):**
  `python benchmark.py`

### 4. Quy ước

- **Input:** Hai số nguyên `n`, `k` thỏa mãn `0 <= k <= n`. (Theo phiếu giới hạn `n <= 8`, hệ thống mở rộng giới hạn `n` động từ 8 đến 12 tùy chế độ để bảo vệ RAM).
- **Thứ tự chỉ số:** Thuật toán lõi sử dụng chỉ số 1-based (bắt đầu từ 1) để đồng bộ với giả mã trong giáo trình. Mảng `x` kích thước `k+1`, mảng `used` kích thước `n+1`.
- **Output:** Danh sách các mảng chỉnh hợp (VD: `[[1, 2], [1, 3]...]`), sắp xếp theo đúng thứ tự từ điển. Với trường hợp biên `k=0`, trả về danh sách chứa mảng rỗng `[[]]`.
- **Xử lý lỗi:** Nếu nhập `n < 0`, `k < 0`, `k > n` hoặc nhập chữ cái, Validator sẽ chặn không chạy thuật toán và hiển thị thông báo lỗi màu đỏ trên giao diện.

### 5. Minh chứng

- **Thư mục ảnh:** `docs/anh_ket_qua/` (Chứa đủ 11 ảnh minh chứng từ A01 đến A11).
- **Mã ca kiểm thử & Kết quả:** Chi tiết tại Chương 4 (Bảng 4.1, 4.2) trong file `BaoCao.docx`.
- **SHA chạy C (Commit tạo ra kết quả test):** `[Điền mã SHA C đầy đủ của bạn vào đây]`
- **SHA nộp S (Commit cuối cùng):** Ghi chú chi tiết trong tệp `ThongTinNop.txt` nộp kèm trên Classroom.

---

## 📖 Giới thiệu

Ứng dụng web trực quan hóa bài toán **Liệt kê chỉnh hợp không lặp chập k của n phần tử**, được xây dựng bằng Flask. Ứng dụng không chỉ dừng ở việc hiển thị kết quả mà còn mô phỏng **từng bước chạy của thuật toán đệ quy quay lui (Backtracking)** thông qua hệ thống trace chi tiết.

Ứng dụng tích hợp thêm **Kỹ thuật Unranking (Phân trang siêu tốc)**, **Xuất dữ liệu CSV theo luồng, giảm sử dụng bộ nhớ** có áp dụng ràng buộc, **Gia sư ảo (Quiz Động)** tự tạo câu hỏi từ dữ liệu thực tế, cùng khả năng **tối ưu bộ nhớ bằng Generator** để xử lý các cặp `(n, k)` lớn trên môi trường server yếu (Render Free 512MB).

---

## 🚀 Tính năng nổi bật

### 1. Tối ưu hóa thuật toán lõi

- **Đệ quy quay lui (Backtracking):** Liệt kê chỉnh hợp không lặp chập k.
- **Sinh kế tiếp (Next Permutation):** Phương pháp không đệ quy dùng cho chế độ liệt kê hiệu năng cao.
- **Kỹ thuật Unranking:** Loại bỏ hoàn toàn chi phí duyệt `O(index)` cấu hình trước đó, giúp nhảy thẳng trực tiếp đến trang cần xem với độ phức tạp `O(k*n)`.
- **Kỹ thuật cắt nhánh (Branch and Bound):** Áp dụng khi có ràng buộc, kèm đo hiệu năng so sánh trực quan với phương pháp "Sinh rồi lọc".

### 2. Trực quan hóa (Visualizer) & Giới hạn động

- Mô phỏng từng bước chạy của thuật toán: `CALL`, `LOOP`, `SELECT`, `SKIP`, `SAVE`, `BACKTRACK`.
- **Điều khiển linh hoạt:** Bước trước / Bước tiếp / Tự động chạy / Đến cuối / Reset. Tốc độ (100ms – 2000ms).
- **Giới hạn `n` động thông minh:** Ràng buộc `n ≤ 8`; Chỉ liệt kê `n ≤ 10`; Học từng bước `n ≤ 11`; Chỉ đếm `n ≤ 12`.

### 3. Xuất dữ liệu CSV (Mở rộng)

- Hỗ trợ tải xuống danh sách chỉnh hợp dưới dạng file `.csv`.
- **Xuất CSV theo luồng (Streaming), giảm sử dụng bộ nhớ & Chuẩn hóa `csv.writer`:** Định dạng chuẩn, không bị lỗi tách cột khi mở bằng Excel (đã tích hợp BOM UTF-8).
- **Cơ chế bảo vệ Server (Custom Modal & Backend Validation):** Chặn cứng giới hạn `n <= 12`, `n <= 8` (nếu có ràng buộc) và `MAX_ROWS = 2.000.000` ở cả Frontend (Modal cảnh báo) lẫn API Backend để tránh sập server.

### 4. Gia sư ảo - Quiz Động (Dynamic Quiz Generator)

- Tự động phân tích trạng thái của trace tại một bước ngẫu nhiên để sinh câu hỏi trắc nghiệm.
- Phản hồi trực quan: Tô xanh đáp án đúng, tô đỏ đáp án sai kèm giải thích chi tiết.

### 5. Kiểm tra tính đúng đắn (Validation)

- Chạy bộ test tự động đối chiếu với thư viện chuẩn `itertools`.
- **Thuật toán so sánh song song (zip_longest):** Tiêu tốn O(1) RAM.
- **Giới hạn `n ≤ 8` cho Validation:** Để đảm bảo không bị Timeout trên server Render Free.

### 6. Benchmark & Đo đạc hiệu năng thực tế (`benchmark.py`)

- **Đo thời gian độc lập:** Dùng `time.perf_counter` lặp 10 lần, lấy trung vị bằng `statistics.median`.
- **Đo bộ nhớ (Peak RAM):** Dùng `tracemalloc` (chỉ đo lường bộ nhớ cấp phát ở mức Python - Python-level allocations) đo độc lập tại trang đầu và trang cuối.
- **Kiểm tra biên tự động:** Chuyển các ca kiểm tra biên (trang 0, trang âm, per_page sai, rank ngoài phạm vi) sang `assert` unit test.

### 7. Giao diện & Trải nghiệm người dùng (UI/UX)

- 3 cột layout, Responsive hoàn toàn, Dark/Light Mode (lưu `localStorage`, chống FOUC).
- Phân trang thông minh (50 kết quả/trang).

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ |
| ------------ | ----------- |
| **Backend** | Python 3.11, Flask, SQLite3 |
| **Frontend** | HTML5, CSS3, JavaScript thuần |
| **Database** | SQLite (Local) |
| **Testing** | Pytest |
| **Deployment** | Docker, Docker Compose, Render |
| **Thuật toán** | Backtracking, Next Permutation, Branch & Bound, Generator, Unranking |

---

## 📂 Cấu trúc thư mục

```text
chinh_hop_app/
├── static/
│   └── style.css               # Toàn bộ CSS
├── templates/
│   └── index.html              # Giao diện chính
├── docs/
│   └── anh_ket_qua/            # Chứa 11 ảnh minh chứng A01 - A11
├── tests/
│   └── test_logic.py           # Bộ unit test (21 ca)
├── app.py                      # Flask server & APIs
├── logic.py                    # Thuật toán lõi, trace, generator, unranking
├── benchmark.py                # Script đo đạc hiệu năng và test biên (assert)
├── requirements.txt            # Danh sách thư viện
├── Dockerfile                  
└── docker-compose.yml          
```

---

## ⚙️ Hướng dẫn cài đặt & Chạy

### 🔹 Cách 1: Chạy trực tiếp (Local)

```bash
pip install -r requirements.txt
python app.py
```

Truy cập giao diện tại: **<http://localhost:5000>**

### 🔹 Cách 2: Chạy bằng Docker

```bash
docker compose up --build
```

---

## 🧪 Chạy kiểm thử & Benchmark

> ⚠️ Lưu ý: Cần kích hoạt môi trường ảo (Conda/Venv) đã cài đủ thư viện trước khi chạy test.

**1. Chạy Unit Test (hiển thị log Input/Expected/Actual):**

```bash
pytest tests/test_logic.py -v -s
```

**2. Chạy đo đạc hiệu năng (Benchmark & Assert biên):**

```bash
python benchmark.py
```

---

## 🌐 RESTful API

### 1. Liệt kê chỉnh hợp

`GET /api/permutations?n=3&k=2` (Giới hạn `n ≤ 8`).

### 2. Kiểm tra tính đúng đắn

`GET /api/verify?n=4&k=2` (Giới hạn `n ≤ 8`).

### 3. Xuất dữ liệu CSV (Stream)

`GET /api/export?n=10&k=2&co_rang_buoc=0`

- **Điều kiện:** `n ≤ 12` (hoặc `n ≤ 8` nếu `co_rang_buoc=1`). Tổng số dòng ≤ 2.000.000. Nếu vi phạm trả về mã `400`.

---

## ⚠️ Giới hạn & Lưu ý kỹ thuật

- **Giới hạn `n` linh hoạt**: Hệ thống tự động điều chỉnh giới hạn nhập `n` (từ 8 đến 12) tùy chế độ để bảo vệ RAM server Render.
- **Kỹ thuật Unranking**: Giúp thời gian tải bất kỳ trang nào đều rất nhanh, loại bỏ điểm yếu của `itertools.islice`.
- **Giới hạn xuất file CSV**: Hệ thống chặn không cho tải file nếu vượt quá 2.000.000 dòng (khoảng 50MB) để tránh tràn RAM (OOM) server 512MB.
- **Ràng buộc mặc định**: `not_first: 1` (A không đầu), `not_adjacent: (2, 3)` (B-C không cạnh).

---

## 🚢 Triển khai Online (Live Demo)

👉 **<https://chinh-hop-app.onrender.com/>**

---

## 👨‍💻 Tác giả

| Thông tin | Chi tiết |
| ----------- | ---------- |
| **Họ và tên** | Vũ Duy Khánh |
| **MSSV** | N24DCDT039 |
| **Lớp** | D24CQDT01-N |
| **Môn học** | Cấu trúc Dữ liệu và Giải thuật (INT13185) |
| **Học viện** | Học viện Công nghệ Bưu chính Viễn thông (PTIT) |

---

## 📝 License

Dự án phục vụ mục đích học tập trong khuôn khổ môn học INT13185 – PTIT.
