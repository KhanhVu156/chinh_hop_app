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

def test_doi_chieu_sinh_va_de_quy():
    # Kiểm tra chéo: 2 thuật toán phải ra kết quả giống hệt nhau
    assert liet_ke_chinh_hop(4, 2) == sinh_ke_tiep_chinh_hop(4, 2)
    assert liet_ke_chinh_hop(4, 4) == sinh_ke_tiep_chinh_hop(4, 4)