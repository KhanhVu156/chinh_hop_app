import pytest
from logic import (so_chinh_hop, liet_ke_chinh_hop, sinh_ke_tiep_chinh_hop, 
                   liet_ke_sinh_roi_loc, liet_ke_cat_nhanh,
                   sinh_ke_tiep_chinh_hop_generator, liet_ke_chinh_hop_co_trace, 
                   kiem_tra_tinh_dung)

# ==============================================================================
# 1. NHÓM TEST CƠ BẢN (Hàm tính toán và sinh kế tiếp)
# ==============================================================================
def test_so_chinh_hop():
    assert so_chinh_hop(4, 2) == 12
    assert so_chinh_hop(3, 0) == 1
    assert so_chinh_hop(3, 4) == 0

def test_liet_ke_chinh_hop():
    res = liet_ke_chinh_hop(3, 2)
    assert len(res) == 6
    assert [1, 2] in res
    assert [3, 2] in res

def test_doi_chieu_sinh_va_de_quy_1():
    assert liet_ke_chinh_hop(4, 2) == sinh_ke_tiep_chinh_hop(4, 2)

def test_doi_chieu_sinh_va_de_quy_2():
    assert liet_ke_chinh_hop(4, 4) == sinh_ke_tiep_chinh_hop(4, 4)

# ==============================================================================
# 2. NHÓM TEST BIÊN VÀ DỮ LIỆU SAI (Đáp ứng yêu cầu đề bài)
# ==============================================================================
def test_BIEN01():
    assert liet_ke_chinh_hop(1, 1) == [[1]]
    
def test_BIEN02():
    # Trường hợp k > n
    assert liet_ke_chinh_hop(3, 4) == []
    
def test_BIEN03():
    # Trường hợp k = 0
    assert liet_ke_chinh_hop(0, 0) == [[]]
    
def test_LOI01():
    # Trường hợp n âm
    assert liet_ke_chinh_hop(-1, 2) == []

# ==============================================================================
# 3. NHÓM TEST BỔ SUNG VÀ TỰ THIẾT KẾ
# ==============================================================================
def test_KT01():
    assert len(liet_ke_chinh_hop(4, 2)) == 12
    
def test_KT02():
    assert len(liet_ke_chinh_hop(4, 4)) == 24
    
def test_KT03():
    assert liet_ke_chinh_hop(2, 2) == [[1, 2], [2, 1]]
    
def test_KT04():
    assert liet_ke_chinh_hop(3, 1) == [[1], [2], [3]]
    
def test_TK01():
    assert liet_ke_chinh_hop(5, 3) == sinh_ke_tiep_chinh_hop(5, 3)

# ==============================================================================
# 4. NHÓM TEST RÀNG BUỘC (Cắt nhánh vs Sinh rồi lọc)
# ==============================================================================
def test_RANG_BUOC_1():
    rang_buoc = {'not_first': 1, 'not_adjacent': (2, 3)}
    kq_sinh, _ = liet_ke_sinh_roi_loc(4, 2, rang_buoc)
    kq_cat, _ = liet_ke_cat_nhanh(4, 2, rang_buoc)
    assert kq_sinh == kq_cat
    assert len(kq_cat) == 7 # Bài toán mẫu trong tài liệu

def test_RANG_BUOC_2():
    rang_buoc = {'not_first': 1, 'not_adjacent': (2, 3)}
    kq_sinh, _ = liet_ke_sinh_roi_loc(5, 2, rang_buoc)
    kq_cat, _ = liet_ke_cat_nhanh(5, 2, rang_buoc)
    assert kq_sinh == kq_cat
    assert len(kq_cat) == 14

# ==============================================================================
# 5. NHÓM TEST BIG UPDATE (Generator, Trace, Validation tối ưu)
# ==============================================================================
def test_GENERATOR_01():
    """Kiểm tra Generator sinh ra kết quả giống hệt hàm List truyền thống."""
    gen_result = list(sinh_ke_tiep_chinh_hop_generator(4, 2))
    list_result = sinh_ke_tiep_chinh_hop(4, 2)
    assert gen_result == list_result

def test_GENERATOR_02():
    """Kiểm tra trường hợp biên k=0 với Generator."""
    gen_result = list(sinh_ke_tiep_chinh_hop_generator(5, 0))
    assert gen_result == [[]]

def test_TRACE_01():
    """Kiểm tra Visualizer tạo trace chính xác số bước (max_steps)."""
    _, trace = liet_ke_chinh_hop_co_trace(5, 3, max_steps=50)
    assert len(trace) == 50
    assert trace[0]["type"] == "CALL" # Bước đầu tiên phải là gọi đệ quy

def test_TRACE_02():
    """Kiểm tra trường hợp nhỏ hơn max_steps."""
    _, trace = liet_ke_chinh_hop_co_trace(2, 2, max_steps=1000)
    # n=2, k=2 số bước thực tế sinh ra khoảng 20 bước
    assert len(trace) < 1000
    assert trace[-1]["type"] == "BACKTRACK" # Kết thúc bằng quay lui

def test_VALIDATION_01():
    """Kiểm tra tính đúng đắn (Hàm Streaming O(1) RAM)."""
    results = kiem_tra_tinh_dung(4, 2)
    all_passed = all(r["status"] for r in results)
    assert all_passed is True

def test_VALIDATION_02():
    """Kiểm tra trường hợp k=0 trong Validation."""
    results = kiem_tra_tinh_dung(3, 0)
    all_passed = all(r["status"] for r in results)
    assert all_passed is True