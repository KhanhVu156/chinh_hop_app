import time
import itertools
import io
import csv
import tracemalloc
import statistics
from logic import lay_phan_tu_cua_trang, sinh_ke_tiep_chinh_hop_generator, so_chinh_hop, unrank_chinh_hop

def do_thoi_gian(func, *args, runs=10):
    """Đo thời gian chạy, lặp lại 10 lần và lấy trung vị"""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return statistics.median(times)

def test_kiem_tra_bien_voi_assert():
    """Kiểm tra các ca biên bằng assert để đảm bảo tính đúng đắn"""
    print("--- KIỂM TRA BIÊN VÀ GIỚI HẠN (ASSERT) ---")
    
    # -------------------------------------------------------------------------
    # Ca 1: Trường hợp k = 0
    # Mục đích: Đảm bảo khi chọn 0 phần tử, hàm trả về đúng 1 dãy rỗng [[]]
    # -------------------------------------------------------------------------
    res_k0 = lay_phan_tu_cua_trang(5, 0, 1)
    print(f"Ca 1 (k=0): Actual = {res_k0}, Expected = [[]]")
    assert res_k0 == [[]], f"Lỗi ca 1: Kỳ vọng [[]], nhận được {res_k0}"

    # -------------------------------------------------------------------------
    # Ca 2: Truy xuất phần tử ở trang cuối cùng (Trang 303 của n=9, k=5)
    # Mục đích: Kiểm tra xem hàm có lấy đúng 20 phần tử cuối cùng không
    # -------------------------------------------------------------------------
    n, k = 9, 5
    total = so_chinh_hop(n, k)
    total_pages = (total + 49) // 50
    res_303 = lay_phan_tu_cua_trang(n, k, total_pages)
    print(f"Ca 2 (Trang cuối {total_pages}): Actual = {len(res_303)} phần tử, Expected = 20")
    assert len(res_303) == 20, f"Lỗi ca 2: Kỳ vọng 20 phần tử, nhận được {len(res_303)}"

    # -------------------------------------------------------------------------
    # Ca 3: Truy xuất trang số 0
    # Mục đích: Chặn lỗi truyền sai tham số trang (phải >= 1)
    # -------------------------------------------------------------------------
    res_page0 = lay_phan_tu_cua_trang(n, k, 0)
    print(f"Ca 3 (page=0): Actual = {res_page0}, Expected = []")
    assert res_page0 == [], "Lỗi ca 3: Trang 0 phải trả về []"

    # -------------------------------------------------------------------------
    # Ca 4: Truy xuất trang âm
    # Mục đích: Chặn lỗi truyền tham số trang âm
    # -------------------------------------------------------------------------
    res_page_am = lay_phan_tu_cua_trang(n, k, -1)
    print(f"Ca 4 (page=-1): Actual = {res_page_am}, Expected = []")
    assert res_page_am == [], "Lỗi ca 4: Trang âm phải trả về []"

    # -------------------------------------------------------------------------
    # Ca 5: Truyền kích thước trang per_page = 0
    # Mục đích: Chặn lỗi chia cho 0 hoặc vòng lặp vô hạn khi per_page không hợp lệ
    # -------------------------------------------------------------------------
    res_perpage0 = lay_phan_tu_cua_trang(n, k, 1, per_page=0)
    print(f"Ca 5 (per_page=0): Actual = {res_perpage0}, Expected = []")
    assert res_perpage0 == [], "Lỗi ca 5: per_page=0 phải trả về []"

    # -------------------------------------------------------------------------
    # Ca 6: Unranking với chỉ số (index) âm
    # Mục đích: Đảm bảo hàm unrank không bị lỗi index out of bounds
    # -------------------------------------------------------------------------
    res_unrank_am = unrank_chinh_hop(n, k, -1)
    print(f"Ca 6 (unrank index=-1): Actual = {res_unrank_am}, Expected = None")
    assert res_unrank_am is None, "Lỗi ca 6: Index âm phải trả về None"

    # -------------------------------------------------------------------------
    # Ca 7: Unranking với chỉ số (index) vượt quá tổng số cấu hình
    # Mục đích: Đảm bảo hàm unrank chặn truy cập ngoài phạm vi mảng
    # -------------------------------------------------------------------------
    res_unrank_vuot = unrank_chinh_hop(n, k, total)
    print(f"Ca 7 (unrank index={total}): Actual = {res_unrank_vuot}, Expected = None")
    assert res_unrank_vuot is None, f"Lỗi ca 7: Index vượt quá {total} phải trả về None"
    
    # -------------------------------------------------------------------------
    # Ca 8: Unranking với k=0 và chỉ số (index) âm
    # Mục đích: Theo góp ý của thầy, k=0 thì A(n,0)=1 nên chỉ index=0 là hợp lệ.
    # Các index âm phải bị chặn và trả về None (thay vì trả về []).
    # -------------------------------------------------------------------------
    res_unrank_k0_am = unrank_chinh_hop(5, 0, -1)
    print(f"Ca 8 (unrank k=0, index=-1): Actual = {res_unrank_k0_am}, Expected = None")
    assert res_unrank_k0_am is None, "Lỗi ca 8: k=0, index âm phải trả về None"

    # -------------------------------------------------------------------------
    # Ca 9: Unranking với k=0 và chỉ số (index) vượt quá (index=1)
    # Mục đích: Tương tự ca 8, với k=0, index lớn hơn 0 phải trả về None.
    # -------------------------------------------------------------------------
    res_unrank_k0_vuot = unrank_chinh_hop(5, 0, 1)
    print(f"Ca 9 (unrank k=0, index=1): Actual = {res_unrank_k0_vuot}, Expected = None")
    assert res_unrank_k0_vuot is None, "Lỗi ca 9: k=0, index vượt quá phải trả về None"
    
    print("-> TẤT CẢ CÁC CA KIỂM TRA BIÊN ĐỀU PASS!\n")

def test_hieu_nang():
    n, k = 9, 5
    total_pages = (so_chinh_hop(n, k) + 49) // 50
    
    print("--- SO SÁNH THỜI GIAN (Median) ---")
    for p in [1, 150, total_pages]:
        def chay_islice():
            gen = sinh_ke_tiep_chinh_hop_generator(n, k)
            list(itertools.islice(gen, (p-1)*50, p*50))
        t_islice = do_thoi_gian(chay_islice)
        t_unrank = do_thoi_gian(lay_phan_tu_cua_trang, n, k, p)
        print(f"Trang {p:3d}: islice = {t_islice:7.2f} ms | Unrank = {t_unrank:6.2f} ms")
        
    print("\n--- ĐO THỜI GIAN TẠO CSV TẠI CHỖ (n=10, k=4) ---")
    n, k = 10, 4
    def tao_csv():
        data = io.StringIO()
        writer = csv.writer(data)
        writer.writerow(['STT', 'Chỉnh hợp'])
        data.seek(0); data.truncate(0)
        count = 1
        for day in sinh_ke_tiep_chinh_hop_generator(n, k):
            day_str = "[" + ", ".join(map(str, day)) + "]"
            writer.writerow([count, day_str])
            _ = data.getvalue()
            data.seek(0); data.truncate(0)
            count += 1
    t_csv = do_thoi_gian(tao_csv, runs=5)
    print(f"-> Thời gian tạo luồng CSV: {t_csv:.2f} ms")

def test_ram_tieu_thu():
    print("\n--- ĐO LƯỢNG RAM TIÊU THỤ (Peak Memory) ---")
    n, k = 9, 5
    page = (so_chinh_hop(n, k) + 49) // 50

    tracemalloc.start()
    gen = sinh_ke_tiep_chinh_hop_generator(n, k)
    list(itertools.islice(gen, (page-1)*50, page*50))
    _, peak_islice = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    lay_phan_tu_cua_trang(n, k, page)
    _, peak_unrank = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Trang {page} (n={n}, k={k}): ")
    print(f"  -> islice   : Peak RAM = {peak_islice / 1024:.2f} KB")
    print(f"  -> Unranking: Peak RAM = {peak_unrank / 1024:.2f} KB")

if __name__ == "__main__":
    test_kiem_tra_bien_voi_assert()
    test_hieu_nang()
    test_ram_tieu_thu()