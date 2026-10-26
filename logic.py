import math
import time
import itertools

# ==============================================================================
# BÀI TOÁN: LIỆT KÊ CHỈNH HỢP KHÔNG LẶP CHẬP K CỦA N PHẦN TỬ
# Tư duy giải thuật: 
# - Đệ quy quay lui (Backtracking): Xây dựng dãy x có k phần tử, mảng used 
#   đánh dấu. Tại vị trí i, thử các giá trị chưa dùng, gọi đệ quy i+1, 
#   rồi hoàn tác (backtrack).
# - Sinh kế tiếp (Next Permutation): Từ cấu hình hiện tại, tìm vị trí phải nhất 
#   có thể tăng giá trị, sau đó đặt lại hậu tố về giá trị nhỏ nhất.
# ==============================================================================

def so_chinh_hop(n, k):
    """Tính số lượng chỉnh hợp chập k của n: A(n,k) = n! / (n-k)!"""
    if k < 0 or k > n:
        return 0
    if k == 0:
        return 1
    return math.factorial(n) // math.factorial(n - k)

def thu_chinh_hop(i, k, n, x, used, ket_qua, elements=None):
    """Hàm đệ quy thử các giá trị cho vị trí thứ i."""
    # Điều kiện dừng: Đã điền đủ k vị trí
    if i > k:
        res = [elements[v-1] if elements else v for v in x[1:]]
        ket_qua.append(res) 
        return

    # Thử các giá trị từ 1 đến n
    for j in range(1, n + 1):
        if not used[j]:
            # Tư duy: Chọn j cho vị trí i
            x[i] = j
            used[j] = True 
            
            # Đệ quy xử lý vị trí tiếp theo
            thu_chinh_hop(i + 1, k, n, x, used, ket_qua, elements)
            
            # Tư duy: Quay lui (Backtrack) - Bỏ đánh dấu để nhánh khác dùng lại
            used[j] = False

def liet_ke_chinh_hop(n, k, elements=None):
    """Hàm chính khởi tạo và gọi đệ quy."""
    if k < 0 or k > n:
        return []
    x = [0] * (k + 1)
    used = [False] * (n + 1)
    ket_qua = []
    thu_chinh_hop(1, k, n, x, used, ket_qua, elements)
    return ket_qua

def sinh_ke_tiep_chinh_hop(n, k):
    """
    Phần tự chọn: Sinh chỉnh hợp bằng phương pháp Sinh kế tiếp (không đệ quy).
    """
    if k == 0:
        return [[]]
    if k > n:
        return []

    x = list(range(1, k + 1))
    ket_qua = [list(x)]
    
    while True:
        i = k - 1
        while i >= 0:
            found_next = False
            for v in range(x[i] + 1, n + 1):
                if v not in x[0:i]:
                    x[i] = v
                    found_next = True
                    break
            if found_next:
                break
            i -= 1
        
        if i < 0:
            break
            
        for j in range(i + 1, k):
            val = 1
            while val in x[0:j]:
                val += 1
            x[j] = val
            
        ket_qua.append(list(x))
    
    return ket_qua

def sinh_ke_tiep_chinh_hop_generator(n, k):
    """
    MỞ RỘNG 3: Tối ưu bộ nhớ bằng Generator.
    Thay vì trả về toàn bộ List, hàm yield từng chỉnh hợp.
    """
    if k == 0:
        yield []
        return
    if k > n:
        return

    x = list(range(1, k + 1))
    yield list(x)
    
    while True:
        i = k - 1
        while i >= 0:
            found_next = False
            for v in range(x[i] + 1, n + 1):
                if v not in x[0:i]:
                    x[i] = v
                    found_next = True
                    break
            if found_next:
                break
            i -= 1
        
        if i < 0:
            break
            
        for j in range(i + 1, k):
            val = 1
            while val in x[0:j]:
                val += 1
            x[j] = val
            
        yield list(x)

# ==============================================================================
# HÀM TẠO TRACE CHO VISUALIZER (MÔ PHỎNG)
# ==============================================================================
class StopTrace(Exception):
    pass

def liet_ke_chinh_hop_co_trace(n, k, max_steps=1000): 
    if k < 0 or k > n: return [], []
    x = [0] * (k + 1)
    used = [False] * (n + 1)
    trace = []
    call_stack = []

    def add_trace(step_type, message, pseudo_line):
        if len(trace) < max_steps:
            trace.append({
                "type": step_type, 
                "x": list(x[1:]), 
                "used": list(used[1:]), 
                "stack": list(call_stack),
                "pseudo_line": pseudo_line,
                "message": message
            })
            if len(trace) >= max_steps:
                raise StopTrace()

    def thu_co_trace(i):
        call_stack.append(i)
        add_trace("CALL", f"Gọi đệ quy thu({i})", 1)

        if i > k:
            add_trace("SAVE", f"Đã điền đủ {k} vị trí. Lưu kết quả: {x[1:]}", 2)
            call_stack.pop()
            return

        for j in range(1, n + 1):
            add_trace("LOOP", f"Xét phần tử j = {j}", 4)
            if not used[j]:
                x[i] = j
                used[j] = True
                add_trace("SELECT", f"Chọn {j} cho vị trí {i}, đánh dấu used[{j}]", 6)
                
                thu_co_trace(i + 1)
                
                used[j] = False
                add_trace("BACKTRACK", f"Quay lui: Bỏ chọn {j}, bỏ đánh dấu used[{j}]", 8)
            else:
                add_trace("SKIP", f"Bỏ qua j = {j} vì used[{j}] đang True", 5)
        call_stack.pop()

    try:
        thu_co_trace(1)
    except StopTrace:
        pass 

    return [], trace 

# ==============================================================================
# MỞ RỘNG: XỬ LÝ RÀNG BUỘC VÀ ĐO HIỆU NĂNG
# ==============================================================================

def kiem_tra_rang_buoc(day, rang_buoc):
    if not rang_buoc: return True
    if 'not_first' in rang_buoc and len(day) > 0 and day[0] == rang_buoc['not_first']:
        return False
    if 'not_adjacent' in rang_buoc:
        a, b = rang_buoc['not_adjacent']
        for i in range(len(day) - 1):
            if (day[i] == a and day[i+1] == b) or (day[i] == b and day[i+1] == a):
                return False
    return True

def liet_ke_sinh_roi_loc(n, k, rang_buoc=None):
    tat_ca = liet_ke_chinh_hop(n, k)
    if not rang_buoc: return tat_ca, 0
    
    hop_le = []
    so_nhanh_loai = 0
    for day in tat_ca:
        if kiem_tra_rang_buoc(day, rang_buoc):
            hop_le.append(day)
        else:
            so_nhanh_loai += 1
    return hop_le, so_nhanh_loai

def liet_ke_cat_nhanh(n, k, rang_buoc=None):
    if k < 0 or k > n: return [], 0
    x = [0] * (k + 1)
    used = [False] * (n + 1)
    ket_qua = []
    so_nhanh_cat = 0
    
    def thu(i):
        nonlocal so_nhanh_cat
        if i > k:
            ket_qua.append(list(x[1:]))
            return
        for j in range(1, n + 1):
            if not used[j]:
                hop_le = True
                if rang_buoc:
                    if i == 1 and 'not_first' in rang_buoc and j == rang_buoc['not_first']:
                        hop_le = False
                    if i > 1 and 'not_adjacent' in rang_buoc:
                        a, b = rang_buoc['not_adjacent']
                        if (x[i-1] == a and j == b) or (x[i-1] == b and j == a):
                            hop_le = False
                
                if hop_le:
                    x[i] = j
                    used[j] = True
                    thu(i + 1)
                    used[j] = False
                else:
                    so_nhanh_cat += 1
    thu(1)
    return ket_qua, so_nhanh_cat

def do_hieu_qua(n, k, rang_buoc=None):
    start1 = time.perf_counter()
    kq1, so_nhanh_loai = liet_ke_sinh_roi_loc(n, k, rang_buoc)
    time1 = (time.perf_counter() - start1) * 1000
    
    start2 = time.perf_counter()
    kq2, so_nhanh_cat = liet_ke_cat_nhanh(n, k, rang_buoc)
    time2 = (time.perf_counter() - start2) * 1000
    
    return {
        "sinh_roi_loc": {"so_nghiem": len(kq1), "thoi_gian_ms": round(time1, 4), "nhanh_loai": so_nhanh_loai},
        "cat_nhanh": {"so_nghiem": len(kq2), "thoi_gian_ms": round(time2, 4), "nhanh_loai": so_nhanh_cat},
        "hop_le": kq1 == kq2
    }

# ==============================================================================
# KIỂM TRA TÍNH ĐÚNG ĐẮN (VALIDATION)
# ==============================================================================
def kiem_tra_tinh_dung(n, k):
    results = []
    if k < 0 or k > n:
        return [{"name": "Tham số không hợp lệ", "status": False}]

    if k == 0:
        c = list(sinh_ke_tiep_chinh_hop_generator(n, k))
        s = list(itertools.permutations(range(1, n+1), k))
        results.append({"name": "Trường hợp biên k=0 trả về [[]]", "status": c == [[]]})
        results.append({"name": "Đối chiếu chéo với thư viện chuẩn itertools", "status": c == [list(x) for x in s]})
        return results

    so_luong_ly_thuyet = so_chinh_hop(n, k)
    custom_gen = sinh_ke_tiep_chinh_hop_generator(n, k)
    standard_gen = itertools.permutations(range(1, n+1), k)
    
    count = 0
    valid_length = True
    unique_in_perm = True
    in_range = True
    match_itertools = True
    
    try:
        for custom_item, std_item in itertools.zip_longest(custom_gen, standard_gen):
            if custom_item is None or std_item is None:
                match_itertools = False
                break
                
            count += 1
            if len(custom_item) != k: valid_length = False
            if len(set(custom_item)) != k: unique_in_perm = False
            if not all(1 <= x <= n for x in custom_item): in_range = False
            
            if tuple(custom_item) != std_item:
                match_itertools = False
                break
    except Exception as e:
        return [{"name": "Lỗi khi chạy kiểm tra", "status": False, "msg": str(e)}]
        
    results.append({
        "name": f"Số lượng nghiệm khớp A(n,k) (Thực tế: {count} / Lý thuyết: {so_luong_ly_thuyet})", 
        "status": count == so_luong_ly_thuyet and match_itertools
    })
    results.append({"name": "Mỗi nghiệm có đúng k phần tử", "status": valid_length})
    results.append({"name": "Các phần tử trong 1 nghiệm không lặp lại", "status": unique_in_perm})
    results.append({"name": "Các phần tử đều thuộc khoảng [1, n]", "status": in_range})
    results.append({"name": "Danh sách không có 2 nghiệm trùng nhau", "status": match_itertools})
    results.append({"name": "Đối chiếu chéo với thư viện chuẩn itertools", "status": match_itertools})
    
    return results

# ==============================================================================
# MỞ RỘNG SIÊU TỐC: KỸ THUẬT UNRANKING VÀ PHÂN TRANG
# ==============================================================================
def unrank_chinh_hop(n, k, index):
    """
    Tư duy Unranking: Truy xuất trực tiếp chỉnh hợp thứ `index` (tính từ 0)
    bằng toán học thay vì duyệt tuần tự.
    
    Độ phức tạp: 
    - Bỏ qua được chi phí duyệt O(index) cấu hình trước đó.
    - Tuy nhiên, bản thân hàm tốn O(k*n) do vòng lặp k lần và phép list.pop() tốn O(n).
    """
    if k == 0: return []
    
    # Góp ý 3: Kiểm tra rank ngoài phạm vi (âm hoặc vượt quá A(n,k))
    if index < 0 or index >= so_chinh_hop(n, k):
        return None
        
    chua_dung = list(range(1, n + 1))
    ket_qua = []
    
    for i in range(k):
        # Số lượng chỉnh hợp có thể tạo ra nếu cố định tiền tố hiện tại
        block_size = so_chinh_hop(n - i - 1, k - i - 1)
        if block_size == 0:
            block_size = 1
            
        # Xác định xem phần tử thứ i nên là gì dựa vào index
        chi_so = index // block_size
        index = index % block_size
        
        val = chua_dung.pop(chi_so) # Lưu ý: pop() tốn O(n)
        ket_qua.append(val)
        
    return ket_qua

def sinh_ke_tiep_tu_cau_hinh(n, k, x):
    """Từ một cấu hình x, sinh ra cấu hình kế tiếp trong thứ tự từ điển."""
    x = list(x)
    i = k - 1
    while i >= 0:
        found_next = False
        for v in range(x[i] + 1, n + 1):
            if v not in x[0:i]:
                x[i] = v
                found_next = True
                break
        if found_next:
            break
        i -= 1
    
    if i < 0:
        return None # Đã là cấu hình cuối cùng
        
    for j in range(i + 1, k):
        val = 1
        while val in x[0:j]:
            val += 1
        x[j] = val
        
    return x

def lay_phan_tu_cua_trang(n, k, page, per_page=50):
    """
    Lấy 50 phần tử của trang bằng Unranking + Sinh kế tiếp.
    Tư duy: 
    1. Dùng Unranking để nhảy thẳng đến cấu hình đầu tiên của trang.
    2. Dùng sinh kế tiếp để lấy 49 cấu hình còn lại.
    """
    # Góp ý 3: Chặn các tham số trang và kích thước trang không hợp lệ
    if page <= 0 or per_page <= 0:
        return []

    start_idx = (page - 1) * per_page
    total = so_chinh_hop(n, k)
    
    # Kiểm tra nếu vượt quá tổng số trang hợp lệ
    if start_idx >= total or total == 0:
        return []
        
    # Sửa lỗi theo góp ý trước của thầy: k=0 phải trả về [[]] thay vì []
    if k == 0:
        return [[]]

    # 1. Nhảy thẳng đến phần tử đầu tiên của trang
    first_item = unrank_chinh_hop(n, k, start_idx)
    
    # Dùng "is None" thay vì "not first_item" vì [] là falsy
    if first_item is None: 
        return []
        
    result = [first_item]
    
    # 2. Sinh tiếp 49 phần tử còn lại
    current = first_item
    for _ in range(per_page - 1):
        current = sinh_ke_tiep_tu_cau_hinh(n, k, current)
        if current is None:
            break
        result.append(current)
        
    return result

def do_hieu_qua_phan_trang(n, k, page, per_page=50):
    """Hàm đo đạc hiệu năng so sánh giữa islice và Unranking (Dùng cho báo cáo)"""
    start_idx = (page - 1) * per_page
    
    # Cách 1: islice (duyệt tuần tự)
    start1 = time.perf_counter()
    gen = sinh_ke_tiep_chinh_hop_generator(n, k)
    res_islice = list(itertools.islice(gen, start_idx, start_idx + per_page))
    time_islice = (time.perf_counter() - start1) * 1000
    
    # Cách 2: Unranking + Sinh kế tiếp
    start2 = time.perf_counter()
    res_unrank = lay_phan_tu_cua_trang(n, k, page, per_page)
    time_unrank = (time.perf_counter() - start2) * 1000
    
    return {
        "islice_ms": round(time_islice, 4),
        "unrank_ms": round(time_unrank, 4),
        "khop_nhau": res_islice == res_unrank
    }