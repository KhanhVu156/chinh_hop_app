import pytest
from logic import (so_chinh_hop, liet_ke_chinh_hop, sinh_ke_tiep_chinh_hop, 
                   liet_ke_sinh_roi_loc, liet_ke_cat_nhanh)

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

def test_BIEN01():
    assert liet_ke_chinh_hop(1, 1) == [[1]]
    
def test_BIEN02():
    assert liet_ke_chinh_hop(3, 4) == []
    
def test_BIEN03():
    assert liet_ke_chinh_hop(0, 0) == [[]]
    
def test_LOI01():
    assert liet_ke_chinh_hop(-1, 2) == []

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

# Bổ sung test cho ràng buộc
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