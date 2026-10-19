from flask import Flask, render_template, request, jsonify, g
import sqlite3
# Import thêm 2 hàm mới xử lý ràng buộc
from logic import (so_chinh_hop, liet_ke_chinh_hop, sinh_ke_tiep_chinh_hop, 
                   liet_ke_chinh_hop_co_trace, liet_ke_cat_nhanh, do_hieu_qua)
import os

app = Flask(__name__)
DATABASE = 'history.db'

# ==============================================================================
# QUẢN LÝ DATABASE (Lưu lịch sử)
# ==============================================================================
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        # Cập nhật thêm cột co_rang_buoc và che_do cho bảng history
        db.execute('''CREATE TABLE IF NOT EXISTS history 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       n INTEGER, k INTEGER, so_luong INTEGER, 
                       co_rang_buoc INTEGER DEFAULT 0,
                       che_do TEXT DEFAULT 'hoc',
                       thoi_gian TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        db.commit()

if not os.path.exists(DATABASE):
    init_db()

def luu_lich_su(n, k, so_luong, co_rang_buoc, che_do):
    db = get_db()
    # Thử thêm cột nếu database đã tồn tại từ phiên bản cũ
    try:
        db.execute('ALTER TABLE history ADD COLUMN co_rang_buoc INTEGER DEFAULT 0')
        db.execute('ALTER TABLE history ADD COLUMN che_do TEXT DEFAULT "hoc"')
    except sqlite3.OperationalError:
        pass # Cột đã tồn tại
        
    db.execute('INSERT INTO history (n, k, so_luong, co_rang_buoc, che_do) VALUES (?, ?, ?, ?, ?)', 
               (n, k, so_luong, 1 if co_rang_buoc else 0, che_do))
    db.commit()

# ==============================================================================
# HÀM TÍNH DẢI PHÂN TRANG THÔNG MINH (SMART PAGINATION)
# ==============================================================================
def get_pagination_range(current_page, total_pages, window=2):
    if total_pages <= (window * 2) + 5:
        return range(1, total_pages + 1)
        
    pages = set()
    pages.add(1)
    pages.add(total_pages)
    
    for i in range(max(1, current_page - window), min(total_pages, current_page + window) + 1):
        pages.add(i)
        
    sorted_pages = sorted(list(pages))
    result = []
    for i, p in enumerate(sorted_pages):
        if i > 0 and p - sorted_pages[i-1] > 1:
            result.append("...")
        result.append(p)
    return result

# ==============================================================================
# LUỒNG XỬ LÝ CHÍNH (Giao diện)
# ==============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    ket_qua_de_quy = []
    ket_qua_sinh = []
    trace_data = []
    trace_truncated = False
    n, k, so_luong = 0, 0, 0
    error = None
    da_chay = False
    so_sanh = None
    
    page = request.args.get('page', 1, type=int)
    per_page = 50

    n_str = request.form.get('n') if request.method == 'POST' else request.args.get('n')
    k_str = request.form.get('k') if request.method == 'POST' else request.args.get('k')
    
    # Lấy tham số chế độ hiển thị và ràng buộc
    che_do = request.form.get('che_do') if request.method == 'POST' else request.args.get('che_do', 'hoc')
    co_rang_buoc = (request.form.get('co_rang_buoc') == 'on') if request.method == 'POST' else (request.args.get('co_rang_buoc') == '1')

    if n_str is not None and k_str is not None:
        try:
            n = int(n_str)
            k = int(k_str)
            da_chay = True
            
            if request.method == 'POST':
                page = 1
                
            if n < 0 or n > 8:
                error = "Vui lòng nhập n trong khoảng 0 đến 8."
            elif k < 0 or k > n:
                error = "Vui lòng nhập k thỏa mãn 0 <= k <= n."
            else:
                so_luong = so_chinh_hop(n, k)
                
                # Xử lý logic dựa trên ràng buộc
                if co_rang_buoc:
                    # Ràng buộc mẫu: 1 không đứng đầu, 2 và 3 không đứng cạnh nhau
                    rang_buoc = {'not_first': 1, 'not_adjacent': (2, 3)}
                    full_de_quy, _ = liet_ke_cat_nhanh(n, k, rang_buoc)
                    so_sanh = do_hieu_qua(n, k, rang_buoc)
                    trace_data = [] # Tạm thời ẩn mô phỏng khi có ràng buộc để tránh xung đột
                    
                    # Map số sang ký tự A, B, C, D... để hiển thị đẹp hơn
                    chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                    full_de_quy = [[chars[v-1] for v in day] for day in full_de_quy]
                else:
                    full_de_quy = liet_ke_chinh_hop(n, k)
                    if k > 0 and che_do == 'hoc':
                        full_sinh = sinh_ke_tiep_chinh_hop(n, k)
                        ket_qua_sinh = full_sinh[:per_page]
                        _, trace_data = liet_ke_chinh_hop_co_trace(n, k, max_steps=5000)
                        if len(trace_data) >= 5000:
                            trace_truncated = True
                
                # Phân trang
                if che_do != 'dem':
                    total_pages = (len(full_de_quy) + per_page - 1) // per_page
                    start_idx = (page - 1) * per_page
                    end_idx = start_idx + per_page
                    ket_qua_de_quy = full_de_quy[start_idx:end_idx]
                else:
                    ket_qua_de_quy = []
                    total_pages = 1
                
                if request.method == 'POST':
                    luu_lich_su(n, k, so_luong, co_rang_buoc, che_do)
                    
        except ValueError:
            error = "Dữ liệu nhập vào không hợp lệ."
            
    if 'total_pages' not in locals():
        total_pages = 1

    page_range = get_pagination_range(page, total_pages)

    db = get_db()
    try:
        lich_su = db.execute('SELECT * FROM history ORDER BY id DESC LIMIT 5').fetchall()
    except sqlite3.OperationalError:
        # Trường hợp db cũ chưa được update cột
        lich_su = []

    return render_template('index.html', 
                           n=n, k=k, so_luong=so_luong, 
                           ket_qua_de_quy=ket_qua_de_quy,
                           ket_qua_sinh=ket_qua_sinh,
                           trace_data=trace_data,
                           trace_truncated=trace_truncated,
                           lich_su=lich_su,
                           error=error, da_chay=da_chay,
                           page=page, total_pages=total_pages,
                           page_range=page_range,
                           co_rang_buoc=co_rang_buoc, so_sanh=so_sanh,
                           che_do=che_do)

# ==============================================================================
# RESTFUL API 
# ==============================================================================
@app.route('/api/permutations', methods=['GET'])
def api_permutations():
    try:
        n = int(request.args.get('n', 0))
        k = int(request.args.get('k', 0))
        
        if n < 0 or n > 8 or k < 0 or k > n:
            return jsonify({"error": "Invalid input. Require 0 <= k <= n <= 8."}), 400
            
        so_luong = so_chinh_hop(n, k)
        ket_qua = liet_ke_chinh_hop(n, k)
        
        return jsonify({
            "status": "success",
            "n": n,
            "k": k,
            "count": so_luong,
            "data": ket_qua
        })
    except ValueError:
        return jsonify({"error": "Invalid parameter type."}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)