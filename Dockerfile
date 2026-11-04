# Sử dụng Python 3.11 bản rút gọn
FROM python:3.11-slim

# Tạo thư mục làm việc trong container
WORKDIR /app

# Copy file requirements và cài đặt thư viện trước 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code còn lại vào container
COPY . .

# Mở cổng 5000
EXPOSE 5000

# Lệnh chạy ứng dụng
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]