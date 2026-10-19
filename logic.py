import math
import time

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

def thu_chinh_hop(i, k, n, x, used, ket_qua):
    """Hàm đệ quy thử các giá trị cho vị trí thứ i."""
    # Điều kiện dừng: Đã điền đủ k vị trí
    if i > k:
        # Lưu lại bản sao của dãy hiện tại (tránh tham chiếu bị thay đổi)
        ket_qua.append(list(x[1:])) 
        return

    # Thử các giá trị từ 1 đến n
    for j in range(1, n + 1):
        if not used[j]:
            # Tư duy: Chọn j cho vị trí i
            x[i] = j
            used[j] = True # Đánh dấu đã dùng
            
            # Đệ quy xử lý vị trí tiếp theo
            thu_chinh_hop(i + 1, k, n, x, used, ket_qua)
            
            # Tư duy: Quay lui (Backtrack)
            # Sau khi thử xong nhánh với j, ta phải bỏ đánh dấu để 
            # các nhánh khác có thể sử dụng lại giá trị j.
            used[j] = False

def liet_ke_chinh_hop(n, k):
    """Hàm chính khởi tạo và gọi đệ quy."""
    if k < 0 or k > n:
        return []
    x = [0] * (k + 1) # Mảng 1-based
    used = [False] * (n + 1) # Mảng 1-based
    ket_qua = []
    thu_chinh_hop(1, k, n, x, used, ket_qua)
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
            break # Đã là cấu hình cuối cùng
            
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
def liet_ke_chinh_hop_co_trace(n, k, max_steps=5000):
    """
    Tương tự hàm đệ quy gốc nhưng ghi lại trạng thái từng bước.
    Trả về danh sách các bước để Frontend vẽ animation.
    TỐI ƯU: Thêm tham số max_steps để giới hạn số bước ghi lại,
    tránh tạo ra hàng trăm nghìn bước gây treo trình duyệt.
    """
    if k < 0 or k > n: return [], []
    
    x = [0] * (k + 1)
    used = [False] * (n + 1)
    ket_qua = []
    trace = []

    def thu_co_trace(i):
        # TỐI ƯU: Chỉ ghi trace nếu chưa vượt quá max_steps
        if len(trace) < max_steps:
            trace.append({
                "type": "CALL", 
                "x": list(x[1:]), 
                "used": list(used[1:]), 
                "message": f"Gọi đệ quy tại vị trí i = {i}"
            })

        if i > k:
            ket_qua.append(list(x[1:]))
            if len(trace) < max_steps:
                trace.append({
                    "type": "SAVE", 
                    "x": list(x[1:]), 
                    "used": list(used[1:]), 
                    "message": f"Đã điền đủ {k} vị trí. Lưu kết quả: {x[1:]}"
                })
            return

        for j in range(1, n + 1):
            if not used[j]:
                # Bước chọn
                x[i] = j
                used[j] = True
                if len(trace) < max_steps:
                    trace.append({
                        "type": "SELECT", 
                        "x": list(x[1:]), 
                        "used": list(used[1:]), 
                        "message": f"Thử chọn {j} cho vị trí {i}"
                    })
                
                thu_co_trace(i + 1)
                
                # Bước quay lui
                used[j] = False
                if len(trace) < max_steps:
                    trace.append({
                        "type": "BACKTRACK", 
                        "x": list(x[1:]), 
                        "used": list(used[1:]), 
                        "message": f"Quay lui: Bỏ đánh dấu {j} tại vị trí {i}"
                    })

    thu_co_trace(1)
    return ket_qua, trace

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
    if not rang_buoc: return tat_ca
    return [day for day in tat_ca if kiem_tra_rang_buoc(day, rang_buoc)]

def liet_ke_cat_nhanh(n, k, rang_buoc=None):
    """Phương pháp 2: Quay lui có cắt nhánh (kiểm tra ràng buộc ngay khi xây dựng)."""
    if k < 0 or k > n: return []
    x = [0] * (k + 1)
    used = [False] * (n + 1)
    ket_qua = []
    
    def thu(i):
        if i > k:
            ket_qua.append(list(x[1:]))
            return
        for j in range(1, n + 1):
            if not used[j]:
                hop_le = True
                if rang_buoc:
                    # Cắt nhánh sớm: Nếu vi phạm, không đi tiếp nhánh này
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
    thu(1)
    return ket_qua

def do_hieu_qua(n, k, rang_buoc=None):
    """Đo thời gian và so sánh 2 phương pháp."""
    start1 = time.perf_counter()
    kq1 = liet_ke_sinh_roi_loc(n, k, rang_buoc)
    time1 = (time.perf_counter() - start1) * 1000
    
    start2 = time.perf_counter()
    kq2 = liet_ke_cat_nhanh(n, k, rang_buoc)
    time2 = (time.perf_counter() - start2) * 1000
    
    return {
        "sinh_roi_loc": {"so_nghiem": len(kq1), "thoi_gian_ms": round(time1, 4)},
        "cat_nhanh": {"so_nghiem": len(kq2), "thoi_gian_ms": round(time2, 4)},
        "hop_le": kq1 == kq2
    }