import time
import tracemalloc
from logic import lay_phan_tu_cua_trang, sinh_ke_tiep_chinh_hop_generator

def test_toc_do_trang(n, k, page):
    print(f"--- TEST TỐC ĐỘ TẢI TRANG (Unranking) ---")
    print(f"Cấu hình: n={n}, k={k}, Trang {page}")
    
    tracemalloc.start()
    start_time = time.perf_counter()
    
    # Sử dụng hàm Unranking
    ket_qua = lay_phan_tu_cua_trang(n, k, page)
    
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"-> Thời gian chạy: {(end_time - start_time) * 1000:.2f} ms")
    print(f"-> Bộ nhớ đỉnh (Peak RAM): {peak / 10**6:.4f} MB")
    print(f"-> Số lượng kết quả lấy ra: {len(ket_qua)}\n")

def test_csv(n, k):
    print(f"--- TEST XUẤT FILE CSV ---")
    print(f"Cấu hình: n={n}, k={k}")
    
    start_time = time.perf_counter()
    count = 0
    for day in sinh_ke_tiep_chinh_hop_generator(n, k):
        _ = "[" + ", ".join(map(str, day)) + "]"
        count += 1
        
    end_time = time.perf_counter()
    
    print(f"-> Thời gian tạo luồng dữ liệu: {(end_time - start_time) * 1000:.2f} ms")
    print(f"-> Tổng số dòng sẽ xuất ra: {count}\n")

if __name__ == "__main__":
    print("=====================================================")
    print(" BÁO CÁO HIỆU NĂNG ")
    print("=====================================================\n")

    # Test Unranking với trang đầu
    test_toc_do_trang(10, 10, 1)
    
    # Test Unranking với trang cực xa
    test_toc_do_trang(10, 10, 10000) 
    
    # Test Stream CSV
    test_csv(10, 4) 