import pytest
from logic import (so_chinh_hop, liet_ke_chinh_hop, sinh_ke_tiep_chinh_hop, 
                   liet_ke_sinh_roi_loc, liet_ke_cat_nhanh,
                   sinh_ke_tiep_chinh_hop_generator, liet_ke_chinh_hop_co_trace, 
                   kiem_tra_tinh_dung)

# ==============================================================================
# 1. NHÓM TEST CƠ BẢN (Hàm tính toán và sinh kế tiếp)
# ==============================================================================

def test_VD01_so_chinh_hop():
    """[Ca VD01] Đối tượng: Hàm so_chinh_hop. Input: n=4,k=2 / n=3,k=0 / n=3,k=4. Expected: 12, 1, 0"""
    assert so_chinh_hop(4, 2) == 12
    assert so_chinh_hop(3, 0) == 1
    assert so_chinh_hop(3, 4) == 0

def test_VD02_liet_ke_chinh_hop():
    """[Ca VD02] Đối tượng: Hàm liet_ke_chinh_hop. Input: n=3, k=2. Expected: Trả về 6 dãy"""
    res = liet_ke_chinh_hop(3, 2)
    assert len(res) == 6
    assert [1, 2] in res
    assert [3, 2] in res

def test_TK01_doi_chieu_sinh_va_de_quy_1():
    """[Ca TK01] Đối tượng: Đối chiếu chéo 2 thuật toán. Input: n=4, k=2. Expected: Kết quả Đệ quy == Sinh kế tiếp"""
    assert liet_ke_chinh_hop(4, 2) == sinh_ke_tiep_chinh_hop(4, 2)

def test_TK02_doi_chieu_sinh_va_de_quy_2():
    """[Ca TK02] Đối tượng: Đối chiếu chéo 2 thuật toán. Input: n=4, k=4. Expected: Kết quả Đệ quy == Sinh kế tiếp"""
    assert liet_ke_chinh_hop(4, 4) == sinh_ke_tiep_chinh_hop(4, 4)


# ==============================================================================
# 2. NHÓM TEST BIÊN VÀ DỮ LIỆU SAI (Đáp ứng yêu cầu đề bài)
# ==============================================================================

def test_BIEN01_kich_thuoc_nho_nhat():
    """[Ca BIEN01] Đối tượng: Hàm chính. Input: n=1, k=1. Expected: Trả về [[1]]"""
    assert liet_ke_chinh_hop(1, 1) == [[1]]
    
def test_BIEN02_k_lon_hon_n():
    """[Ca BIEN02] Đối tượng: Hàm chính. Input: n=3, k=4 (k > n). Expected: Trả về danh sách rỗng []"""
    assert liet_ke_chinh_hop(3, 4) == []
    
def test_BIEN03_k_bang_0():
    """[Ca BIEN03] Đối tượng: Hàm chính. Input: n=0, k=0. Expected: Trả về danh sách chứa 1 mảng rỗng [[]]"""
    assert liet_ke_chinh_hop(0, 0) == [[]]
    
def test_LOI01_input_sai_n_am():
    """[Ca LOI01] Đối tượng: Hàm chính. Input: n=-1, k=2 (Dữ liệu sai). Expected: Trả về danh sách rỗng []"""
    assert liet_ke_chinh_hop(-1, 2) == []


# ==============================================================================
# 3. NHÓM TEST BỔ SUNG VÀ TỰ THIẾT KẾ
# ==============================================================================

def test_KT09_kiem_tra_do_dai_4_2():
    """[Ca KT09] Đối tượng: Hàm chính. Input: n=4, k=2. Expected: Độ dài mảng kết quả bằng 12"""
    assert len(liet_ke_chinh_hop(4, 2)) == 12
    
def test_KT10_kiem_tra_do_dai_4_4():
    """[Ca KT10] Đối tượng: Hàm chính. Input: n=4, k=4. Expected: Độ dài mảng kết quả bằng 24"""
    assert len(liet_ke_chinh_hop(4, 4)) == 24
    
def test_KT11_kiem_tra_gia_tri_2_2():
    """[Ca KT11] Đối tượng: Hàm chính. Input: n=2, k=2. Expected: [[1, 2], [2, 1]]"""
    assert liet_ke_chinh_hop(2, 2) == [[1, 2], [2, 1]]
    
def test_KT12_kiem_tra_gia_tri_3_1():
    """[Ca KT12] Đối tượng: Hàm chính. Input: n=3, k=1. Expected: [[1], [2], [3]]"""
    assert liet_ke_chinh_hop(3, 1) == [[1], [2], [3]]
    
def test_KT13_doi_chieu_mo_rong_5_3():
    """[Ca KT13] Đối tượng: Đối chiếu 2 thuật toán. Input: n=5, k=3. Expected: Kết quả Đệ quy == Sinh kế tiếp"""
    assert liet_ke_chinh_hop(5, 3) == sinh_ke_tiep_chinh_hop(5, 3)


# ==============================================================================
# 4. NHÓM TEST RÀNG BUỘC (Cắt nhánh vs Sinh rồi lọc)
# ==============================================================================

def test_KT14_rang_buoc_4_2():
    """[Ca KT14] Đối tượng: Cắt nhánh vs Sinh lọc. Input: n=4, k=2 có ràng buộc. Expected: 2 phương pháp cho kết quả giống nhau (7 dãy)"""
    rang_buoc = {'not_first': 1, 'not_adjacent': (2, 3)}
    kq_sinh, _ = liet_ke_sinh_roi_loc(4, 2, rang_buoc)
    kq_cat, _ = liet_ke_cat_nhanh(4, 2, rang_buoc)
    assert kq_sinh == kq_cat
    assert len(kq_cat) == 7

def test_KT15_rang_buoc_5_2():
    """[Ca KT15] Đối tượng: Cắt nhánh vs Sinh lọc. Input: n=5, k=2 có ràng buộc. Expected: 2 phương pháp cho kết quả giống nhau (14 dãy)"""
    rang_buoc = {'not_first': 1, 'not_adjacent': (2, 3)}
    kq_sinh, _ = liet_ke_sinh_roi_loc(5, 2, rang_buoc)
    kq_cat, _ = liet_ke_cat_nhanh(5, 2, rang_buoc)
    assert kq_sinh == kq_cat
    assert len(kq_cat) == 14


# ==============================================================================
# 5. NHÓM TEST BIG UPDATE (Generator, Trace, Validation tối ưu)
# ==============================================================================

def test_KT16_generator_4_2():
    """[Ca KT16] Đối tượng: Hàm Generator. Input: n=4, k=2. Expected: Kết quả Generator == Kết quả hàm List truyền thống"""
    gen_result = list(sinh_ke_tiep_chinh_hop_generator(4, 2))
    list_result = sinh_ke_tiep_chinh_hop(4, 2)
    assert gen_result == list_result

def test_KT17_generator_bien_k_0():
    """[Ca KT17] Đối tượng: Hàm Generator. Input: n=5, k=0. Expected: Trả về [[]]"""
    gen_result = list(sinh_ke_tiep_chinh_hop_generator(5, 0))
    assert gen_result == [[]]

def test_KT18_trace_gioi_han_buoc():
    """[Ca KT18] Đối tượng: Visualizer Trace. Input: n=5, k=3, max_steps=50. Expected: Độ dài trace = 50, bước đầu là 'CALL'"""
    _, trace = liet_ke_chinh_hop_co_trace(5, 3, max_steps=50)
    assert len(trace) == 50
    assert trace[0]["type"] == "CALL"

def test_KT19_trace_duoi_gioi_han():
    """[Ca KT19] Đối tượng: Visualizer Trace. Input: n=2, k=2, max_steps=1000. Expected: Độ dài trace < 1000, bước cuối là 'BACKTRACK'"""
    _, trace = liet_ke_chinh_hop_co_trace(2, 2, max_steps=1000)
    assert len(trace) < 1000
    assert trace[-1]["type"] == "BACKTRACK"

def test_KT20_validation_4_2():
    """[Ca KT20] Đối tượng: Hàm Validation. Input: n=4, k=2. Expected: Tất cả tiêu chí đúng (all_passed = True)"""
    results = kiem_tra_tinh_dung(4, 2)
    all_passed = all(r["status"] for r in results)
    assert all_passed is True

def test_KT21_validation_3_0():
    """[Ca KT21] Đối tượng: Hàm Validation. Input: n=3, k=0. Expected: Tất cả tiêu chí đúng (all_passed = True)"""
    results = kiem_tra_tinh_dung(3, 0)
    all_passed = all(r["status"] for r in results)
    assert all_passed is True