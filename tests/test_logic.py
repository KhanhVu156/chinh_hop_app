import pytest
from logic import (so_chinh_hop, liet_ke_chinh_hop, sinh_ke_tiep_chinh_hop, 
                   liet_ke_sinh_roi_loc, liet_ke_cat_nhanh,
                   sinh_ke_tiep_chinh_hop_generator, liet_ke_chinh_hop_co_trace, 
                   kiem_tra_tinh_dung)

def in_ket_qua(ma_ca, doi_tuong, input_str, expected, actual, is_pass):
    """Hàm hỗ trợ in log ra Terminal cho đẹp"""
    print("\n" + "="*70)
    print(f"MÃ CA     : {ma_ca}")
    print(f"ĐỐI TƯỢNG : {doi_tuong}")
    print(f"INPUT     : {input_str}")
    print(f"EXPECTED  : {expected}")
    print(f"ACTUAL    : {actual}")
    print(f"KẾT LUẬN  : {'PASS' if is_pass else 'FAIL'}")
    print("="*70)

# ==============================================================================
# 1. NHÓM TEST CƠ BẢN (Có ảnh A01 - A02)
# ==============================================================================

def test_VD01_so_chinh_hop():
    ma_ca = "VD01 (Ví dụ 1 phiếu)"
    doi_tuong = "Hàm so_chinh_hop"
    input_str = "n=4,k=2 | n=3,k=0 | n=3,k=4"
    expected = "12 | 1 | 0"
    
    actual_1 = so_chinh_hop(4, 2)
    actual_2 = so_chinh_hop(3, 0)
    actual_3 = so_chinh_hop(3, 4)
    actual = f"{actual_1} | {actual_2} | {actual_3}"
    
    is_pass = (actual_1 == 12) and (actual_2 == 1) and (actual_3 == 0)
    in_ket_qua(ma_ca, doi_tuong, input_str, expected, actual, is_pass)
    
    assert actual_1 == 12
    assert actual_2 == 1
    assert actual_3 == 0

def test_VD02_liet_ke_chinh_hop():
    ma_ca = "VD02 (Ví dụ 2 phiếu)"
    doi_tuong = "Hàm liet_ke_chinh_hop"
    input_str = "n=3, k=2"
    expected = "6 dãy"
    
    res = liet_ke_chinh_hop(3, 2)
    actual = f"{len(res)} dãy"
    
    is_pass = (len(res) == 6) and ([1, 2] in res) and ([3, 2] in res)
    in_ket_qua(ma_ca, doi_tuong, input_str, expected, actual, is_pass)
    
    assert len(res) == 6
    assert [1, 2] in res
    assert [3, 2] in res

# ==============================================================================
# 2. NHÓM TEST TỰ THIẾT KẾ (Có ảnh A03 - A04)
# ==============================================================================

def test_TK01_doi_chieu_sinh_va_de_quy_1():
    ma_ca = "TK01 (Tự thiết kế 1)"
    doi_tuong = "Đối chiếu chéo Đệ quy vs Sinh kế tiếp"
    input_str = "n=4, k=2"
    expected = "Kết quả 2 hàm giống hệt nhau"
    
    kq_de_quy = liet_ke_chinh_hop(4, 2)
    kq_sinh = sinh_ke_tiep_chinh_hop(4, 2)
    
    is_pass = (kq_de_quy == kq_sinh)
    actual = "Giống nhau" if is_pass else "Khác nhau"
    in_ket_qua(ma_ca, doi_tuong, input_str, expected, actual, is_pass)
    
    assert kq_de_quy == kq_sinh

def test_TK02_doi_chieu_sinh_va_de_quy_2():
    ma_ca = "TK02 (Tự thiết kế 2)"
    doi_tuong = "Đối chiếu chéo Đệ quy vs Sinh kế tiếp"
    input_str = "n=4, k=4"
    expected = "Kết quả 2 hàm giống hệt nhau"
    
    kq_de_quy = liet_ke_chinh_hop(4, 4)
    kq_sinh = sinh_ke_tiep_chinh_hop(4, 4)
    
    is_pass = (kq_de_quy == kq_sinh)
    actual = "Giống nhau" if is_pass else "Khác nhau"
    in_ket_qua(ma_ca, doi_tuong, input_str, expected, actual, is_pass)
    
    assert kq_de_quy == kq_sinh

# ==============================================================================
# 3. NHÓM TEST BIÊN VÀ DỮ LIỆU SAI (Có ảnh A05 - A08)
# ==============================================================================

def test_BIEN01_kich_thuoc_nho_nhat():
    ma_ca = "BIEN01"
    doi_tuong = "Hàm chính (Kích thước nhỏ nhất)"
    input_str = "n=1, k=1"
    expected = "[[1]]"
    
    actual = liet_ke_chinh_hop(1, 1)
    is_pass = (actual == [[1]])
    in_ket_qua(ma_ca, doi_tuong, input_str, expected, actual, is_pass)
    
    assert actual == [[1]]
    
def test_BIEN02_k_lon_hon_n():
    ma_ca = "BIEN02"
    doi_tuong = "Hàm chính (k > n)"
    input_str = "n=3, k=4"
    expected = "[] (Danh sách rỗng)"
    
    actual = liet_ke_chinh_hop(3, 4)
    is_pass = (actual == [])
    in_ket_qua(ma_ca, doi_tuong, input_str, expected, actual, is_pass)
    
    assert actual == []
    
def test_BIEN03_k_bang_0():
    ma_ca = "BIEN03"
    doi_tuong = "Hàm chính (k = 0)"
    input_str = "n=0, k=0"
    expected = "[[]] (Mảng chứa 1 dãy rỗng)"
    
    actual = liet_ke_chinh_hop(0, 0)
    is_pass = (actual == [[]])
    in_ket_qua(ma_ca, doi_tuong, input_str, expected, actual, is_pass)
    
    assert actual == [[]]
    
def test_LOI01_input_sai_n_am():
    ma_ca = "LOI01"
    doi_tuong = "Hàm chính (Input không hợp lệ)"
    input_str = "n=-1, k=2"
    expected = "[] (Danh sách rỗng)"
    
    actual = liet_ke_chinh_hop(-1, 2)
    is_pass = (actual == [])
    in_ket_qua(ma_ca, doi_tuong, input_str, expected, actual, is_pass)
    
    assert actual == []


# ==============================================================================
# 4. NHÓM TEST BỔ SUNG (KT09 - KT21)
# Lưu ý: Các ca này không cần chụp ảnh nên có thể để assert trực tiếp.
# ==============================================================================

def test_KT09_kiem_tra_do_dai_4_2():
    assert len(liet_ke_chinh_hop(4, 2)) == 12
    
def test_KT10_kiem_tra_do_dai_4_4():
    assert len(liet_ke_chinh_hop(4, 4)) == 24
    
def test_KT11_kiem_tra_gia_tri_2_2():
    assert liet_ke_chinh_hop(2, 2) == [[1, 2], [2, 1]]
    
def test_KT12_kiem_tra_gia_tri_3_1():
    assert liet_ke_chinh_hop(3, 1) == [[1], [2], [3]]
    
def test_KT13_doi_chieu_mo_rong_5_3():
    assert liet_ke_chinh_hop(5, 3) == sinh_ke_tiep_chinh_hop(5, 3)

def test_KT14_rang_buoc_4_2():
    rang_buoc = {'not_first': 1, 'not_adjacent': (2, 3)}
    kq_sinh, _ = liet_ke_sinh_roi_loc(4, 2, rang_buoc)
    kq_cat, _ = liet_ke_cat_nhanh(4, 2, rang_buoc)
    assert kq_sinh == kq_cat
    assert len(kq_cat) == 7

def test_KT15_rang_buoc_5_2():
    rang_buoc = {'not_first': 1, 'not_adjacent': (2, 3)}
    kq_sinh, _ = liet_ke_sinh_roi_loc(5, 2, rang_buoc)
    kq_cat, _ = liet_ke_cat_nhanh(5, 2, rang_buoc)
    assert kq_sinh == kq_cat
    assert len(kq_cat) == 14

def test_KT16_generator_4_2():
    gen_result = list(sinh_ke_tiep_chinh_hop_generator(4, 2))
    list_result = sinh_ke_tiep_chinh_hop(4, 2)
    assert gen_result == list_result

def test_KT17_generator_bien_k_0():
    gen_result = list(sinh_ke_tiep_chinh_hop_generator(5, 0))
    assert gen_result == [[]]

def test_KT18_trace_gioi_han_buoc():
    _, trace = liet_ke_chinh_hop_co_trace(5, 3, max_steps=50)
    assert len(trace) == 50
    assert trace[0]["type"] == "CALL"

def test_KT19_trace_duoi_gioi_han():
    _, trace = liet_ke_chinh_hop_co_trace(2, 2, max_steps=1000)
    assert len(trace) < 1000
    assert trace[-1]["type"] == "BACKTRACK"

def test_KT20_validation_4_2():
    results = kiem_tra_tinh_dung(4, 2)
    assert all(r["status"] for r in results) is True

def test_KT21_validation_3_0():
    results = kiem_tra_tinh_dung(3, 0)
    assert all(r["status"] for r in results) is True