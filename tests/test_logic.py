import pytest
from logic import so_chinh_hop, liet_ke_chinh_hop, sinh_ke_tiep_chinh_hop

def test_so_chinh_hop():
    # Kiểm tra công thức tính A(n,k)
    assert so_chinh_hop(4, 2) == 12
    assert so_chinh_hop(3, 0) == 1
    assert so_chinh_hop(3, 4) == 0

def test_liet_ke_chinh_hop():
    # Kiểm tra số lượng và tính đúng đắn của thuật toán đệ quy
    res = liet_ke_chinh_hop(3, 2)
    assert len(res) == 6
    assert [1, 2] in res
    assert [3, 2] in res

def test_doi_chieu_sinh_va_de_quy_1():
    # Kiểm tra chéo: 2 thuật toán phải ra kết quả giống hệt nhau (n=4, k=2)
    assert liet_ke_chinh_hop(4, 2) == sinh_ke_tiep_chinh_hop(4, 2)

def test_doi_chieu_sinh_va_de_quy_2():
    # Kiểm tra chéo: 2 thuật toán phải ra kết quả giống hệt nhau (n=4, k=4)
    assert liet_ke_chinh_hop(4, 4) == sinh_ke_tiep_chinh_hop(4, 4)

def test_BIEN01():
    # BIEN01: n=1, k=1
    assert liet_ke_chinh_hop(1, 1) == [[1]]
    
def test_BIEN02():
    # BIEN02: k > n (Lỗi)
    assert liet_ke_chinh_hop(3, 4) == []
    
def test_BIEN03():
    # BIEN03: n=0, k=0
    assert liet_ke_chinh_hop(0, 0) == [[]]
    
def test_LOI01():
    # LOI01: n < 0 (Lỗi)
    assert liet_ke_chinh_hop(-1, 2) == []

def test_KT01():
    # KT01: n=4, k=2
    assert len(liet_ke_chinh_hop(4, 2)) == 12
    
def test_KT02():
    # KT02: n=4, k=4
    assert len(liet_ke_chinh_hop(4, 4)) == 24
    
def test_KT03():
    # KT03: n=2, k=2 (Ví dụ 2 phiếu)
    assert liet_ke_chinh_hop(2, 2) == [[1, 2], [2, 1]]
    
def test_KT04():
    # KT04: n=3, k=1
    assert liet_ke_chinh_hop(3, 1) == [[1], [2], [3]]
    
def test_TK01():
    # TK01: Đối chiếu chéo n=5, k=3
    assert liet_ke_chinh_hop(5, 3) == sinh_ke_tiep_chinh_hop(5, 3)