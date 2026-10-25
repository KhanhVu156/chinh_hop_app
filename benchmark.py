import time
import tracemalloc
import itertools
from logic import (lay_phan_tu_cua_trang, sinh_ke_tiep_chinh_hop_generator, 
                   liet_ke_cat_nhanh, so_chinh_hop)

def test_trang(n, k, page, per_page=50):
    """
    So sánh hiệu năng và đối chiếu tính đúng giữa 2 cách:
    1. Dùng itertools.islice (duyệt tuần tự)
    2. Dùng Unranking + Sinh kế tiếp
    """
    total_items = so_chinh_hop(n, k)
    total_pages = (total_items + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    
    print(f"--- TEST TRANG {page}/{total_pages} (n={n}, k={k}) ---")
    if start_idx >= total_items:
        print("-> Trang vượt quá tổng số trang.\n")
        return

    # CÁCH 1: Dùng islice (Duyệt tuần tự)
    tracemalloc.start()
    start1 = time.perf_counter()
    
    gen = sinh_ke_tiep_chinh_hop_generator(n, k)
    res_islice = list(itertools.islice(gen, start_idx, start_idx + per_page))
    
    end1 = time.perf_counter()
    _, peak_islice = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    time_islice = (end1 - start1) * 1000

    # CÁCH 2: Dùng Unranking + Sinh kế tiếp
    tracemalloc.start()
    start2 = time.perf_counter()
    
    res_unrank = lay_phan_tu_cua_trang(n, k, page, per_page)
    
    end2 = time.perf_counter()
    _, peak_unrank = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    time_unrank = (end2 - start2) * 1000

    # Đối chiếu kết quả
    is_correct = (res_islice == res_unrank)

    print(f"[Cách 1 - islice]    Thời gian: {time_islice:>8.2f} ms | Peak RAM: {peak_islice / 10**6:.4f} MB")
    print(f"[Cách 2 - Unranking] Thời gian: {time_unrank:>8.2f} ms | Peak RAM: {peak_unrank / 10**6:.4f} MB")
    print(f"-> Kết quả 2 cách khớp nhau: {'ĐÚNG' if is_correct else 'SAI LỆCH'}")
    print("-" * 60 + "\n")

def test_csv(n, k, co_rang_buoc=False):
    """Đo hiệu năng xuất CSV bằng Generator/Streaming"""
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
    # Cấu hình test theo đúng phạm vi thầy cho phép (n <= 10)
    n, k = 10, 8
    total_items = so_chinh_hop(n, k)
    total_pages = (total_items + 49) // 50
    
    print(f"=== CẤU HÌNH: n={n}, k={k}, Tổng số hoán vị={total_items}, Tổng số trang={total_pages} ===\n")
    
    # 1. Đo trang đầu
    test_trang(n, k, page=1)
    
    # 2. Đo trang xa (Trang giữa)
    test_trang(n, k, page=total_pages // 2)
    
    # 3. Đo trang cuối
    test_trang(n, k, page=total_pages)
    
    # 4. Đo xuất CSV (n=10, k=4 để ko bị quá lớn)
    test_csv(10, 4, False)      
    test_csv(8, 4, True)        