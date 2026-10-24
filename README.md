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
  `python app.py` (Truy cập `http://localhost:5000` để nhập n, k tùy ý).
- **Lệnh chạy toàn bộ kiểm thử:**
  `pytest test_logic.py -v`

### 4. Quy ước

- **Input:** Hai số nguyên `n`, `k` thỏa mãn `0 <= k <= n`. (Theo phiếu giới hạn `n <= 8`, hệ thống mở rộng giới hạn `n` động từ 8 đến 12 tùy chế độ để bảo vệ RAM).
- **Thứ tự chỉ số:** Thuật toán lõi sử dụng chỉ số **1-based** (bắt đầu từ 1) để đồng bộ với giả mã trong giáo trình. Mảng `x` kích thước `k+1`, mảng `used` kích thước `n+1`.
- **Output:** Danh sách các mảng chỉnh hợp (VD: `[[1, 2], [1, 3]...]`), sắp xếp theo đúng thứ tự từ điển. Với trường hợp biên `k=0`, trả về danh sách chứa mảng rỗng `[[]]`.
- **Xử lý lỗi:** Nếu nhập `n < 0`, `k < 0`, `k > n` hoặc nhập chữ cái, Validator sẽ chặn không chạy thuật toán và hiển thị thông báo lỗi màu đỏ trên giao diện (VD: *"Vui lòng nhập k thỏa mãn 0 <= k <= n"*).

### 5. Minh chứng

- **Thư mục ảnh:** `docs/anh_ket_qua/` (Chứa đủ 11 ảnh minh chứng từ A01 đến A11).
- **Mã ca kiểm thử & Kết quả:** Chi tiết tại Chương 4 (Bảng 4.1, 4.2) trong file `BaoCao.docx`.
- **SHA chạy C (Commit tạo ra kết quả test):** `[Điền mã SHA C đầy đủ của bạn vào đây]`
- **SHA nộp S (Commit cuối cùng):** Ghi chú chi tiết trong tệp `ThongTinNop.txt` nộp kèm trên Classroom.

---

## 📖 Giới thiệu

Ứng dụng web trực quan hóa bài toán **Liệt kê chỉnh hợp không lặp chập k của n phần tử**, được xây dựng bằng Flask. Ứng dụng không chỉ dừng ở việc hiển thị kết quả mà còn mô phỏng **từng bước chạy của thuật toán đệ quy quay lui (Backtracking)** thông qua hệ thống trace chi tiết.

Ứng dụng tích hợp thêm **Kỹ thuật Unranking (Phân trang O(1))**, **Xuất dữ liệu CSV không tốn RAM có áp dụng ràng buộc**, **Gia sư ảo (Quiz Động)** tự tạo câu hỏi từ dữ liệu thực tế, cùng khả năng **tối ưu bộ nhớ bằng Generator** để xử lý các cặp `(n, k)` lớn (lên đến `n=11, 12`) trên môi trường server yếu (Render Free 512MB).

---

## 🚀 Tính năng nổi bật

### 1. Tối ưu hóa thuật toán lõi

- **Đệ quy quay lui (Backtracking)**: Liệt kê chỉnh hợp không lặp chập k.
- **Sinh kế tiếp (Next Permutation)**: Phương pháp không đệ quy dùng cho chế độ liệt kê hiệu năng cao.
- **Kỹ thuật Unranking (Điểm nhấn)**: Thay vì dùng `islice` phải duyệt tuần tự qua hàng triệu phần tử (gây chậm khi xem trang xa), thuật toán Unranking sử dụng toán học để **nhảy thẳng trực tiếp đến trang cần xem** với độ phức tạp **O(1)**. Thời gian tải trang 1 và trang 70.000 đều chỉ mất **< 1ms**.
- **Kỹ thuật cắt nhánh (Branch and Bound)**: Áp dụng khi có ràng buộc, kèm đo hiệu năng so sánh trực quan với phương pháp "Sinh rồi lọc".

### 2. Trực quan hóa (Visualizer) & Giới hạn động

- Mô phỏng **từng bước chạy** của thuật toán: `CALL`, `LOOP`, `SELECT`, `SKIP`, `SAVE`, `BACKTRACK`.
- Hiển thị trực quan: Mảng `x`, mảng `used`, Ngăn xếp lời gọi (Call stack), Mã giả (Pseudo-code) và Nhật ký thực thi.
- **Điều khiển linh hoạt**: Bước trước / Bước tiếp / Tự động chạy / Đến cuối / Reset. Tốc độ (100ms – 2000ms).
- ⚠️ **Giới hạn 1000 bước** mô phỏng đầu tiên để đảm bảo tốc độ hiển thị.
- **Giới hạn `n` động thông minh**:
  - **Chế độ Ràng buộc**: `n ≤ 8` (Sinh toàn bộ mảng).
  - **Chế độ Chỉ liệt kê**: `n ≤ 10` (Dùng Unranking).
  - **Chế độ Học từng bước**: `n ≤ 11` (Chỉ sinh 1000 trace).
  - **Chế độ Chỉ đếm**: `n ≤ 12` (Chỉ tính công thức).

### 3. Xuất dữ liệu CSV (Mở rộng 2)

- Hỗ trợ tải xuống danh sách chỉnh hợp dưới dạng file `.csv`.
- **Áp dụng đúng ràng buộc**: File xuất ra sẽ áp dụng điều kiện (A không đầu, B-C không cạnh) nếu người dùng có tick chọn.
- **Streaming trực tiếp & Chuẩn hóa `csv.writer`**: Dữ liệu được truyền từng dòng, không lưu file vào ổ cứng hay RAM. Định dạng chuẩn, không bị lỗi tách cột khi mở bằng Excel (đã tích hợp BOM UTF-8).
- **Cơ chế bảo vệ Server (Custom Modal)**: Nếu số dòng vượt quá **2.000.000 dòng**, hệ thống sẽ hiển thị một Modal cảnh báo (được thiết kế đồng bộ với UI) và chặn tải xuống để tránh sập server.

### 4. Gia sư ảo - Quiz Động (Dynamic Quiz Generator)

- Tự động **phân tích trạng thái của trace** (mảng x, used, call stack, dòng mã giả) tại một bước ngẫu nhiên để sinh câu hỏi.
- Hàng ngàn câu hỏi trắc nghiệm khác nhau với độ nhiễu cao.
- Phản hồi trực quan: Tô xanh đáp án đúng, tô đỏ đáp án sai kèm giải thích chi tiết.

### 5. Kiểm tra tính đúng đắn (Validation) - Tối ưu Streaming

- Nhấn nút **"Chạy kiểm tra tính đúng"** để chạy bộ test tự động đối chiếu với thư viện chuẩn `itertools`.
- **Thuật toán so sánh song song (zip_longest)**: Tiêu tốn O(1) RAM thay vì tạo mảng.
- ⚠️ **Giới hạn `n ≤ 8` cho Validation**: Để đảm bảo không bị Timeout (quá 30 giây) trên server Render Free. Nút bấm sẽ tự động ẩn đi khi `n > 8`.

### 6. Giao diện & Trải nghiệm người dùng (UI/UX)

- **3 cột layout**: Cấu hình — Mô phỏng — Nhật ký & Lịch sử.
- **Responsive hoàn toàn**: Tự động xếp dọc giao diện trên màn hình nhỏ (Mobile/Tablet).
- **Dark/Light Mode** lưu vào `localStorage`, chống nháy màu (FOUC).
- **CSS Tối ưu**: Thanh cuộn đồng bộ trên 3 cột, nút bấm tự động co giãn chống tràn layout.
- **Phân trang thông minh** (50 kết quả/trang) dải số trang rút gọn dạng `1 … 5 6 7 … 20`.

### 7. Lưu trữ lịch sử

- Mỗi lần chạy được ghi vào CSDL **SQLite** (bảng `history`).
- Hiển thị 5 lần chạy gần nhất, có nút **Chạy lại**.

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ |
| ------------ | ----------- |
| **Backend** | Python 3.11, Flask, SQLAlchemy (SQLite) |
| **Frontend** | HTML5, CSS3 (CSS Variables, Media Queries), JavaScript thuần |
| **Database** | SQLite (Local) / PostgreSQL (Production) |
| **Testing** | Pytest |
| **Deployment** | Docker, Docker Compose, GitHub Actions (CI/CD), Render |
| **Thuật toán** | Backtracking, Next Permutation, Branch & Bound, Generator, **Unranking**, `csv.writer`, `itertools.zip_longest` |

---

## 📂 Cấu trúc thư mục

```text
chinh_hop_app/
├── .github/workflows/          # Cấu hình CI/CD (tự động chạy test)
├── static/
│   └── style.css               # Toàn bộ CSS (Responsive, Dark/Light Mode, Visualizer...)
├── templates/
│   └── index.html              # Giao diện chính (Visualizer + Dynamic Quiz + Export Modal)
├── tests/                      # Unit test với Pytest
├── app.py                      # Flask server: routes, API, database, phân trang, CSV Stream
├── logic.py                    # Thuật toán lõi, trace, generator, unranking, validation O(1)
├── requirements.txt            # Danh sách thư viện
├── Dockerfile                  # Đóng gói ứng dụng
└── docker-compose.yml          # Cấu hình Docker Compose
```

---

## ⚙️ Hướng dẫn cài đặt & Chạy

### 🔹 Cách 1: Chạy trực tiếp (Local)

```bash
# 1. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 2. Chạy ứng dụng
python app.py
```

Truy cập giao diện tại: **<http://localhost:5000>**

### 🔹 Cách 2: Chạy bằng Docker (Khuyên dùng)

```bash
docker compose up --build
```

Truy cập giao diện tại: **<http://localhost:5000>**

---

## 🧪 Chạy kiểm thử tự động

> ⚠️ **Lưu ý quan trọng**: Trước khi chạy test, cần kích hoạt môi trường ảo (Virtual Environment / Conda) đã cài đủ thư viện trong `requirements.txt`. Khuyến nghị cài **Miniconda** để quản lý môi trường dễ dàng.

### Bước 1: Thiết lập môi trường với Conda

```bash
# Tạo môi trường mới
conda create -n webapp python=3.11 -y

# Kích hoạt (thay 'webapp' bằng tên môi trường thực tế)
conda activate webapp

# Cài đặt thư viện
pip install -r requirements.txt
```

### Bước 2: Chạy kiểm thử

```bash
pytest tests/ -v
```

---

## 🌐 RESTful API

### 1. Liệt kê chỉnh hợp

```http
GET /api/permutations?n=3&k=2
```

**Response mẫu:**

```json
{
  "status": "success",
  "n": 3,
  "k": 2,
  "count": 6,
  "data": [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]
}
```

**Điều kiện hợp lệ:** `0 ≤ k ≤ n ≤ 8`. Nếu sai trả về mã `400`.

### 2. Kiểm tra tính đúng đắn

```http
GET /api/verify?n=4&k=2
```

**Response mẫu:**

```json
{
  "all_passed": true,
  "results": [
    { "name": "Số lượng nghiệm khớp A(n,k) ...", "status": true },
    { "name": "Mỗi nghiệm có đúng k phần tử", "status": true }
  ]
}
```

**Điều kiện hợp lệ:** `0 ≤ k ≤ n ≤ 8` (Giới hạn để tránh Timeout server).

### 3. Xuất dữ liệu CSV (Stream)

```http
GET /api/export?n=10&k=2&co_rang_buoc=0
```

Trả về file `.csv` trực tiếp qua luồng (stream).
**Tham số `co_rang_buoc`**: `1` (Áp dụng ràng buộc) hoặc `0` (Không ràng buộc).
**Điều kiện hợp lệ:** `0 ≤ k ≤ n ≤ 10` và tổng số dòng ≤ 2.000.000.

---

## ⚠️ Giới hạn & Lưu ý kỹ thuật

- **Giới hạn `n` linh hoạt**: Hệ thống tự động điều chỉnh giới hạn nhập `n` (từ 8 đến 12) tùy thuộc vào chế độ nhằm bảo vệ RAM và thời gian phản hồi của Server Render.
- **Kỹ thuật Unranking**: Được áp dụng cho chế độ "Chỉ liệt kê" giúp thời gian tải bất kỳ trang nào (từ trang 1 đến trang 70.000) đều chỉ mất `< 1ms`, loại bỏ hoàn toàn điểm yếu của `itertools.islice`.
- **Giới hạn xuất file CSV**: Hệ thống chặn không cho tải file nếu tổng số dòng vượt quá **2.000.000 dòng**. Lý do là file CSV lúc này sẽ nặng khoảng 50MB, thời gian stream mất ~15 giây, nếu lớn hơn sẽ gây tràn RAM (OOM) server 512MB.
- **Visualizer giới hạn 1.000 bước** mô phỏng đầu tiên. Nếu cần xem toàn bộ kết quả, dùng chế độ **Chỉ liệt kê**.
- **Mô phỏng chỉ khả dụng** ở chế độ **Học từng bước** và **không có ràng buộc**.
- **Ràng buộc mặc định**:
  - `not_first: 1` → Phần tử **A** không được đứng đầu.
  - `not_adjacent: (2, 3)` → **B và C** không được đứng cạnh nhau.

---

## 🚢 Triển khai Online (Live Demo)

Ứng dụng đã được triển khai tự động qua **Render**:

👉 **<https://chinh-hop-app.onrender.com/>**

---

## 👨‍💻 Tác giả

| Thông tin | Chi tiết |
| ----------- | ---------- |
| **Họ và tên** | Vũ Duy Khánh |
| **MSSV** | N24DCDT039 |
| **Lớp** | D24CQDT01-N |
| **Môn học** | Cấu trúc Dữ liệu và Giải thuật (INT13185) |
| **Nhóm** | 03 |
| **Học viện** | Học viện Công nghệ Bưu chính Viễn thông (PTIT) |

---

## 📝 License

Dự án phục vụ mục đích học tập trong khuôn khổ môn học INT13185 – PTIT.
