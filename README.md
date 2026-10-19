# 🎯 Chinh Hop Visualizer App (DT035)

> **Đồ án môn học Cấu trúc Dữ liệu và Giải thuật (INT13185)**  
> Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
> Được thiết kế và mở rộng thành ứng dụng Web trực quan hóa thuật toán (Algorithm Visualizer) chuẩn production.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-brightgreen)](https://chinh-hop-app.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

---

## 📖 Giới thiệu

Ứng dụng web trực quan hóa bài toán **Liệt kê chỉnh hợp không lặp chập k của n phần tử**, được xây dựng bằng Flask. Ứng dụng không chỉ dừng ở việc hiển thị kết quả mà còn mô phỏng **từng bước chạy của thuật toán đệ quy quay lui (Backtracking)** thông qua hệ thống trace chi tiết, kết hợp kiểm tra tính đúng đắn tự động và các bài tập tương tác.

---

## 🚀 Tính năng nổi bật

### 1. Thuật toán lõi
- **Đệ quy quay lui (Backtracking)**: Liệt kê chỉnh hợp không lặp chập k.
- **Sinh kế tiếp (Next Permutation)**: Phương pháp không đệ quy dùng cho chế độ liệt kê hiệu năng cao.
- **Kỹ thuật cắt nhánh (Branch and Bound)**: Áp dụng khi có ràng buộc, kèm đo hiệu năng so sánh với phương pháp "Sinh rồi lọc".

### 2. Trực quan hóa (Visualizer)
- Mô phỏng **từng bước chạy** của thuật toán: `CALL`, `LOOP`, `SELECT`, `SKIP`, `SAVE`, `BACKTRACK`.
- Hiển thị trực quan:
  - **Mảng `x`** (giá trị đang xây dựng).
  - **Mảng `used`** (đánh dấu phần tử đã dùng).
  - **Ngăn xếp lời gọi** (call stack).
  - **Dòng mã giả đang thực thi** (highlight).
  - **Nhật ký thực thi** (log realtime).
- **Điều khiển linh hoạt**: Bước trước / Bước tiếp / Tự động chạy / Đến cuối / Reset.
- **Thanh trượt tốc độ** (100ms – 2000ms).
- ⚠️ **Giới hạn 1000 bước** mô phỏng đầu tiên để đảm bảo hiệu năng; kết quả tính toán vẫn **chính xác toàn bộ**.

### 3. Ba chế độ hiển thị thông minh
| Chế độ | Mô tả |
|--------|-------|
| **Học từng bước** | Chỉ sinh trace để mô phỏng, không sinh mảng kết quả (tránh treo web). |
| **Chỉ liệt kê** | Sinh toàn bộ kết quả bằng phương pháp "Sinh kế tiếp" (nhẹ hơn đệ quy). |
| **Chỉ đếm** | Chỉ trả về số lượng A(n,k), bỏ qua mọi thao tác sinh mảng. |

### 4. Ràng buộc tùy chọn & Đo hiệu năng
Khi bật tùy chọn ràng buộc (A không đứng đầu, B–C không kề nhau), hệ thống tự động:
- Chạy song song 2 phương pháp: **Sinh rồi lọc** vs **Cắt nhánh**.
- Hiển thị bảng so sánh: số nghiệm, số nhánh bị loại, thời gian chạy (ms).

### 5. Kiểm tra tính đúng đắn (Validation)
Nhấn nút **"Chạy kiểm tra tính đúng"** để thực thi bộ test tự động qua endpoint `/api/verify`:
- ✅ Số lượng nghiệm khớp công thức A(n,k).
- ✅ Mỗi nghiệm có đúng k phần tử.
- ✅ Các phần tử trong nghiệm không lặp.
- ✅ Các phần tử thuộc khoảng [1, n].
- ✅ Không có nghiệm trùng lặp.
- ✅ **Đối chiếu chéo với `itertools.permutations`** của Python.
- ✅ Trường hợp biên `k = 0` trả về `[[]]`.

### 6. Luyện tập tương tác (Quiz)
- Tự động **sinh câu hỏi ngẫu nhiên** từ dữ liệu trace.
- Câu hỏi xoay quanh các bước: `SELECT`, `BACKTRACK`, `SAVE`.
- Phản hồi đúng/sai tức thì với giải thích.

### 7. Giao diện & Trải nghiệm người dùng
- **3 cột layout**: Cấu hình — Mô phỏng — Nhật ký & Lịch sử.
- **Responsive**, tự động thích ứng màn hình.
- **Dark/Light Mode** với công tắc gạt:
  - Lưu lựa chọn vào `localStorage`.
  - Chống nháy màu khi tải trang (FOUC).
- **Phân trang thông minh** (50 kết quả/trang) với dải số trang rút gọn dạng `1 … 5 6 7 … 20`.

### 8. Lưu trữ lịch sử
- Mỗi lần chạy được ghi vào CSDL **SQLite** (bảng `history`).
- Hiển thị 5 lần chạy gần nhất, có nút **Chạy lại**.
- Lưu kèm: `n`, `k`, `số lượng`, `có ràng buộc`, `chế độ`, `thời gian`.

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ |
|------------|-----------|
| **Backend** | Python 3.11, Flask, SQLAlchemy (SQLite) |
| **Frontend** | HTML5, CSS3 (CSS Variables), JavaScript thuần |
| **Database** | SQLite (Local) / PostgreSQL (Production) |
| **Testing** | Pytest |
| **Deployment** | Docker, Docker Compose, GitHub Actions (CI/CD), Render |
| **Thuật toán** | Backtracking, Next Permutation, Branch & Bound, itertools (đối chiếu) |

---

## 📂 Cấu trúc thư mục

```text
chinh_hop_app/
├── .github/workflows/          # Cấu hình CI/CD (tự động chạy test)
├── static/
│   └── style.css               # Toàn bộ CSS (Light/Dark Mode, Visualizer, Quiz...)
├── templates/
│   └── index.html              # Giao diện chính (3 cột + Quiz + Visualizer)
├── tests/                      # Unit test với Pytest
├── app.py                      # Flask server: routes, API, database, phân trang
├── logic.py                    # Thuật toán lõi, trace, ràng buộc, validation
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

Truy cập giao diện tại: **http://localhost:5000**

### 🔹 Cách 2: Chạy bằng Docker (Khuyên dùng)

```bash
docker compose up --build
```

Truy cập giao diện tại: **http://localhost:5000**

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

---

## ⚠️ Giới hạn & Lưu ý kỹ thuật

- **`n` tối đa = 8** để đảm bảo hiệu năng hiển thị (số chỉnh hợp A(8,k) tối đa 40.320).
- **Visualizer giới hạn 1.000 bước** mô phỏng đầu tiên. Nếu cần xem toàn bộ kết quả, dùng chế độ **Chỉ liệt kê**.
- **Mô phỏng chỉ khả dụng** ở chế độ **Học từng bước** và **không có ràng buộc**.
- **Quiz section** chỉ xuất hiện khi có trace hợp lệ (chế độ học, không ràng buộc).
- Ràng buộc mặc định đang được **hard-code** trong `app.py`:
  - `not_first: 1` → Phần tử **A** không được đứng đầu.
  - `not_adjacent: (2, 3)` → **B và C** không được đứng cạnh nhau.

---

## 🚢 Triển khai Online (Live Demo)

Ứng dụng đã được triển khai tự động qua **Render**:

👉 **https://chinh-hop-app.onrender.com/**

---

## 👨‍💻 Tác giả

| Thông tin | Chi tiết |
|-----------|----------|
| **Họ và tên** | Vũ Duy Khánh |
| **MSSV** | N24DCDT039 |
| **Lớp** | D24CQDT01-N |
| **Môn học** | Cấu trúc Dữ liệu và Giải thuật (INT13185) |
| **Nhóm** | 03 |
| **Học viện** | Học viện Công nghệ Bưu chính Viễn thông (PTIT) |

---

## 📝 License

Dự án phục vụ mục đích học tập trong khuôn khổ môn học INT13185 – PTIT.