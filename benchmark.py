import time
import tracemalloc
import itertools
from logic import sinh_ke_tiep_chinh_hop_generator

def test_cach_cu(n, k):
    print(f"--- TEST CÁCH CŨ (Lưu toàn bộ vào List) ---")
    print(f"Cấu hình: n={n}, k={k}")
    
    tracemalloc.start()
    start_time = time.perf_counter()
    
    # Cách cũ: Sinh toàn bộ mảng
    ket_qua = list(sinh_ke_tiep_chinh_hop_generator(n, k))
    
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"-> Thời gian chạy: {(end_time - start_time) * 1000:.2f} ms")
    print(f"-> Bộ nhớ đỉnh (Peak RAM): {peak / 10**6:.2f} MB")
    print(f"-> Số lượng kết quả: {len(ket_qua)}\n")

def test_cach_moi(n, k, page):
    print(f"--- TEST CÁCH MỚI (Generator + islice) ---")
    print(f"Cấu hình: n={n}, k={k}, Xem trang {page}")
    
    per_page = 50
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    tracemalloc.start()
    start_time = time.perf_counter()
    
    # Cách mới: Dùng islice
    gen = sinh_ke_tiep_chinh_hop_generator(n, k)
    ket_qua = list(itertools.islice(gen, start_idx, end_idx))
    
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"-> Thời gian chạy: {(end_time - start_time) * 1000:.2f} ms")
    print(f"-> Bộ nhớ đỉnh (Peak RAM): {peak / 10**6:.2f} MB")
    print(f"-> Số lượng kết quả lấy ra: {len(ket_qua)}\n")

def test_csv(n, k):
    print(f"--- TEST XUẤT FILE CSV (Dùng Stream) ---")
    print(f"Cấu hình: n={n}, k={k}")
    
    start_time = time.perf_counter()
    count = 0
    # Giả lập quá trình stream file
    for day in sinh_ke_tiep_chinh_hop_generator(n, k):
        _ = "[" + ", ".join(map(str, day)) + "]"
        count += 1
        
    end_time = time.perf_counter()
    
    print(f"-> Thời gian tạo luồng dữ liệu: {(end_time - start_time) * 1000:.2f} ms")
    print(f"-> Tổng số dòng sẽ xuất ra: {count}\n")

if __name__ == "__main__":
    print("=====================================================")
    print(" KẾT QUẢ ĐO HIỆU NĂNG ")
    print("=====================================================\n")

    # 1. Test Cách cũ (Sập RAM)
    test_cach_cu(10, 5) 
    
    # 2. Test Cách mới - Trang đầu (Nhanh)
    test_cach_moi(10, 5, 1)
    
    # 3. Test Cách mới - Trang xa (Chứng minh nhược điểm của islice như Thầy nói)
    # n=10, k=10 có 3.628.800 kết quả -> Xem trang 10.000 phải bỏ qua 500.000 phần tử
    test_cach_moi(10, 10, 10000) 
    
    # 4. Test xuất CSV (Đo thời gian stream)
    test_csv(10, 4) # 5040 kết quả