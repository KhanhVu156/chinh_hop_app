# Chinh Hop Visualizer App (DT035)

Dự án môn học Cấu trúc Dữ liệu và Giải thuật (INT13185) - Học viện Công nghệ Bưu chính Viễn thông.
Được thiết kế và mở rộng thành một ứng dụng Web trực quan hóa thuật toán (Algorithm Visualizer) và đóng gói chuẩn production.

## 🚀 Tính năng nổi bật

- **Thuật toán lõi:** Liệt kê chỉnh hợp không lặp chập k bằng phương pháp Đệ quy Quay lui (Backtracking) và Sinh kế tiếp (Next Permutation).
- **Trực quan hóa (Visualizer):** Mô phỏng từng bước chạy của thuật toán (chọn, quay lui), hiển thị trạng thái mảng `x` và mảng đánh dấu `used` trực quan sinh động.
- **Lịch sử tính toán:** Lưu trữ các lần chạy gần nhất vào cơ sở dữ liệu.
- **RESTful API:** Cung cấp endpoint `/api/permutations` để các ứng dụng bên thứ 3 có thể gọi và lấy dữ liệu dạng JSON.
- **Giao diện:** Responsive, tự động chuyển đổi giữa chế độ Sáng/Tối (Light/Dark Mode) theo cài đặt hệ thống.

## 🛠️ Công nghệ sử dụng

- **Backend:** Python 3.11, Flask, SQLAlchemy
- **Frontend:** HTML, CSS (CSS Variables), JavaScript thuần
- **Database:** SQLite (Local) / PostgreSQL (Production)
- **Testing:** Pytest
- **Deployment:** Docker, Docker Compose, GitHub Actions (CI/CD), Render

## 📂 Cấu trúc thư mục

```text
chinh_hop_app/
├── .github/workflows/  # Cấu hình CI/CD tự động chạy test
├── static/             # File CSS
├── templates/          # File HTML giao diện
├── tests/              # Unit test với Pytest
├── app.py              # Máy chủ Flask (API & Database)
├── logic.py            # Thuật toán lõi & Hàm tạo Trace
├── requirements.txt    # Danh sách thư viện
├── Dockerfile          # Đóng gói ứng dụng
└── docker-compose.yml  # Cấu hình Docker Compose
```

## ⚙️ Hướng dẫn cài đặt & Chạy

### Cách 1: Chạy trực tiếp (Local)

```bash
# 1. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 2. Chạy ứng dụng
python app.py
```

Truy cập giao diện tại: `http://localhost:5000`

### Cách 2: Chạy bằng Docker (Khuyên dùng)

```bash
docker compose up --build
```

Truy cập giao diện tại: `http://localhost:5000`

## 🧪 Chạy kiểm thử tự động

> **⚠️ Lưu ý quan trọng:**
> Trước khi chạy lệnh kiểm thử, bạn cần kích hoạt môi trường ảo (Virtual Environment / Conda) đã cài đặt các thư viện trong `requirements.txt`.
> Nếu máy tính chưa có sẵn, khuyến nghị cài đặt **Miniconda** trước để tạo và quản lý môi trường ảo dễ dàng.

**Bước 1: Thiết lập môi trường với Conda**

```bash
# Tạo môi trường mới (nếu chưa có)
conda create -n webapp python=3.11 -y

# Kích hoạt môi trường (thay 'webapp' bằng tên môi trường thực tế của bạn)
conda activate webapp

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

**Bước 2: Chạy kiểm thử**
Sau khi môi trường đã được kích hoạt và cài đặt đầy đủ, chạy lệnh sau để thực thi toàn bộ test case:

```bash
pytest tests/ -v
```

## 🌐 Triển khai Online (Live Demo)

Ứng dụng đã được triển khai tự động qua Render:
👉 **https://chinh-hop-app.onrender.com/**

## 👨‍💻 Tác giả

- **Vũ Duy Khánh** - MSSV: N24DCDT039 - Lớp: D24CQDT01-N
- Môn học: Cấu trúc dữ liệu và Giải thuật (INT13185) - Nhóm 03
