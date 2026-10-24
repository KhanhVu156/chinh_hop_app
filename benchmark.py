import time
import tracemalloc
from logic import lay_phan_tu_cua_trang, sinh_ke_tiep_chinh_hop_generator, liet_ke_cat_nhanh

def test_trang(n, k, page):
    print(f"--- TẢI TRANG {page} (n={n}, k={k}) ---")
    tracemalloc.start()
    start = time.perf_counter()
    
    ket_qua = lay_phan_tu_cua_trang(n, k, page)
    
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"-> Thời gian: {(end - start) * 1000:.2f} ms")
    print(f"-> Peak RAM: {peak / 10**6:.4f} MB\n")

def test_csv(n, k, co_rang_buoc=False):
    print(f"--- XUẤT CSV (n={n}, k={k}, Ràng buộc={co_rang_buoc}) ---")
    start = time.perf_counter()
    count = 0
    if co_rang_buoc:
        res, _ = liet_ke_cat_nhanh(n, k, {'not_first': 1, 'not_adjacent': (2, 3)})
        for _ in res: count += 1
    else:
        for _ in sinh_ke_tiep_chinh_hop_generator(n, k): count += 1
    end = time.perf_counter()
    print(f"-> Thời gian tạo luồng: {(end - start) * 1000:.2f} ms")
    print(f"-> Số dòng: {count}\n")

if __name__ == "__main__":
    test_trang(10, 10, 1)       # Trang đầu (Phải siêu nhanh)
    test_trang(10, 10, 70000)   # Trang xa (Phải < 1ms, không bị 7s như islice)
    test_csv(10, 4, False)      # Xuất CSV thường
    test_csv(8, 4, True)        # Xuất CSV có ràng buộc