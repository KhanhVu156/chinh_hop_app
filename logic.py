import math
import time
import itertools

# ==============================================================================
# BÀI TOÁN: LIỆT KÊ CHỈNH HỢP KHÔNG LẶP CHẬP K CỦA N PHẦN TỬ
# Tư duy: Sử dụng phương pháp Quay lui (Backtracking).
# - Xây dựng dãy x có k phần tử.
# - Tại mỗi vị trí i (từ 1 đến k), thử các giá trị từ 1 đến n.
# - Điều kiện: Giá trị đó chưa được sử dụng (mảng used).
# - Khi đã điền đủ k vị trí, ta thu được 1 chỉnh hợp.
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
    Tư duy: 
    1. Khởi tạo x = [1, 2, ..., k].
    2. Tìm vị trí i bên phải nhất có thể thay đổi. Tại i, tìm giá trị v > x[i] 
       nhỏ nhất mà v chưa xuất hiện trong tiền tố x[0...i-1].
    3. Gán x[i] = v.
    4. Đặt các phần tử phía sau x[i] thành các số nhỏ nhất có thể chưa xuất hiện.
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

# ==============================================================================
# HÀM TẠO TRACE CHO VISUALIZER (MÔ PHỎNG)
# ==============================================================================
class StopTrace(Exception):
    """Exception dùng để ngắt toàn bộ đệ quy ngay lập tức khi đủ số bước."""
    pass

def liet_ke_chinh_hop_co_trace(n, k, max_steps=1000): 
    """Tạo trace mô phỏng từng bước của thuật toán đệ quy."""
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
            # Ngắt ngay lập tức khi đủ số bước yêu cầu
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
        pass # Kết thúc êm đẹp

    return [], trace 

# ==============================================================================
# MỞ RỘNG: XỬ LÝ RÀNG BUỘC VÀ ĐO HIỆU NĂNG
# ==============================================================================

def kiem_tra_rang_buoc(day, rang_buoc):
    """Kiểm tra một dãy hoàn chỉnh có thỏa mãn ràng buộc không."""
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
    """Phương pháp 1: Sinh tất cả chỉnh hợp, sau đó lọc theo ràng buộc."""
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
    """Phương pháp 2: Quay lui có cắt nhánh (kiểm tra ràng buộc ngay khi xây dựng)."""
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
                    # Tư duy cắt nhánh: Kiểm tra sớm, nếu vi phạm thì dừng nhánh này
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
    """Đo thời gian và so sánh 2 phương pháp."""
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
    """Chạy các bài kiểm tra tự động để chứng minh tính đúng của thuật toán."""
    results = []
    try:
        ket_qua = liet_ke_chinh_hop(n, k)
    except Exception as e:
        return [{"name": "Chạy thuật toán", "status": False, "msg": str(e)}]
        
    # 1. Kiểm tra số lượng so với A(n,k)
    so_luong_thuc_te = len(ket_qua)
    so_luong_ly_thuyet = so_chinh_hop(n, k)
    results.append({
        "name": f"Số lượng nghiệm khớp A(n,k) (Thực tế: {so_luong_thuc_te} / Lý thuyết: {so_luong_ly_thuyet})", 
        "status": so_luong_thuc_te == so_luong_ly_thuyet
    })
    
    # 2. Kiểm tra cấu trúc nghiệm
    valid_length = all(len(day) == k for day in ket_qua)
    unique_in_perm = all(len(set(day)) == k for day in ket_qua)
    in_range = all(all(1 <= x <= n for x in day) for day in ket_qua)
    
    results.append({"name": "Mỗi nghiệm có đúng k phần tử", "status": valid_length})
    results.append({"name": "Các phần tử trong 1 nghiệm không lặp lại", "status": unique_in_perm})
    results.append({"name": "Các phần tử đều thuộc khoảng [1, n]", "status": in_range})
    
    # 3. Kiểm tra trùng lặp danh sách
    unique_list = len(set(tuple(x) for x in ket_qua)) == so_luong_thuc_te
    results.append({"name": "Danh sách không có 2 nghiệm trùng nhau", "status": unique_list})
    
    # 4. Đối chiếu với thư viện chuẩn itertools.permutations
    if k > 0:
        it_kq = [list(p) for p in itertools.permutations(range(1, n+1), k)]
        ket_qua_sorted = sorted([tuple(x) for x in ket_qua])
        it_kq_sorted = sorted([tuple(x) for x in it_kq])
        results.append({"name": "Đối chiếu chéo với thư viện chuẩn itertools", "status": ket_qua_sorted == it_kq_sorted})
    else:
        results.append({"name": "Trường hợp biên k=0 trả về [[]]", "status": ket_qua == [[]]})
        
    return results