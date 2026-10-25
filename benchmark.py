import time
import itertools
import io
import csv
import tracemalloc 
from logic import lay_phan_tu_cua_trang, sinh_ke_tiep_chinh_hop_generator, so_chinh_hop

def do_thoi_gian(func, *args, runs=10):
    """Đo thời gian chạy, lặp lại 10 lần và lấy trung vị để chính xác"""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    times.sort()
    return times[len(times) // 2]

def test_trang_va_gioi_han():
    print("--- KIỂM TRA BIÊN VÀ GIỚI HẠN ---")
    
    # Test lỗi k=0 (Thầy góp ý 2)
    res_k0 = lay_phan_tu_cua_trang(5, 0, 1)
    print(f"Test k=0: {res_k0} (Kỳ vọng: [[]])")
    
    # Test vượt số trang (Thầy góp ý 1)
    n, k = 9, 5
    total = so_chinh_hop(n, k) # 15120
    total_pages = (total + 49) // 50 # 303 trang
    page = 303
    res_303 = lay_phan_tu_cua_trang(n, k, page)
    print(f"Test n=9, k=5, page={page}: Lấy được {len(res_303)} phần tử (Kỳ vọng: 20)")
    
    print("\n--- SO SÁNH THỜI GIAN (Median of 10 runs) ---")
    for p in [1, 150, total_pages]: # Đầu, giữa, cuối
        # Đo islice
        def chay_islice():
            gen = sinh_ke_tiep_chinh_hop_generator(n, k)
            list(itertools.islice(gen, (p-1)*50, p*50))
        t_islice = do_thoi_gian(chay_islice)
        
        # Đo unrank
        t_unrank = do_thoi_gian(lay_phan_tu_cua_trang, n, k, p)
        
        print(f"Trang {p:3d}: islice = {t_islice:7.2f} ms | Unrank = {t_unrank:6.2f} ms")

def test_csv_thuc_te():
    print("\n--- ĐO THỜI GIAN TẠO CSV THỰC TẾ (n=10, k=4) ---")
    n, k = 10, 4
    
    def tao_csv():
        # Giả lập quá trình tạo CSV giống hệt trong app.py (dùng csv.writer)
        data = io.StringIO()
        writer = csv.writer(data)
        
        writer.writerow(['STT', 'Chỉnh hợp'])
        data.seek(0)
        data.truncate(0)
        
        count = 1
        for day in sinh_ke_tiep_chinh_hop_generator(n, k):
            day_str = "[" + ", ".join(map(str, day)) + "]"
            writer.writerow([count, day_str])
            _ = data.getvalue() # Giả lập yield ra ngoài
            data.seek(0)
            data.truncate(0)
            count += 1
            
    t_csv = do_thoi_gian(tao_csv, runs=5)
    print(f"-> Thời gian tạo luồng CSV: {t_csv:.2f} ms")

def test_ram_tieu_thu():
    """Hàm đo lượng RAM tiêu thụ (Tách riêng khỏi đo thời gian để đảm bảo độ chính xác)"""
    print("\n--- ĐO LƯỢNG RAM TIÊU THỤ (Peak Memory) ---")
    n, k = 9, 5
    total = so_chinh_hop(n, k)
    total_pages = (total + 49) // 50
    page = total_pages # Đo ở trang cuối (trang xa nhất) để thấy rõ sự khác biệt

    # 1. Đo RAM cho islice (duyệt tuần tự)
    tracemalloc.start()
    gen = sinh_ke_tiep_chinh_hop_generator(n, k)
    list(itertools.islice(gen, (page-1)*50, page*50))
    _, peak_islice = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # 2. Đo RAM cho Unranking
    tracemalloc.start()
    lay_phan_tu_cua_trang(n, k, page)
    _, peak_unrank = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Trang {page} (n={n}, k={k}): ")
    print(f"  -> islice   : Peak RAM = {peak_islice / 1024:.2f} KB")
    print(f"  -> Unranking: Peak RAM = {peak_unrank / 1024:.2f} KB")

if __name__ == "__main__":
    test_trang_va_gioi_han()
    test_csv_thuc_te()
    test_ram_tieu_thu()