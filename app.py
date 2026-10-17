from flask import Flask, render_template, request, jsonify, g
import sqlite3
from logic import so_chinh_hop, liet_ke_chinh_hop, sinh_ke_tiep_chinh_hop, liet_ke_chinh_hop_co_trace
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
        db.execute('''CREATE TABLE IF NOT EXISTS history 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       n INTEGER, k INTEGER, so_luong INTEGER, 
                       thoi_gian TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        db.commit()

# Khởi tạo DB khi chạy lần đầu
if not os.path.exists(DATABASE):
    init_db()

def luu_lich_su(n, k, so_luong):
    db = get_db()
    db.execute('INSERT INTO history (n, k, so_luong) VALUES (?, ?, ?)', (n, k, so_luong))
    db.commit()

# ==============================================================================
# LUỒNG XỬ LÝ CHÍNH (Giao diện)
# ==============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    ket_qua_de_quy = []
    ket_qua_sinh = []
    trace_data = []
    n, k, so_luong = 0, 0, 0
    error = None
    da_chay = False
    
    # Cấu hình Phân trang
    page = request.args.get('page', 1, type=int)
    per_page = 50

    # Lấy n và k từ POST (nếu chạy form) hoặc từ URL (nếu chuyển trang)
    n_str = request.form.get('n') if request.method == 'POST' else request.args.get('n')
    k_str = request.form.get('k') if request.method == 'POST' else request.args.get('k')

    if n_str is not None and k_str is not None:
        try:
            n = int(n_str)
            k = int(k_str)
            da_chay = True
            
            if request.method == 'POST':
                page = 1 # Reset về trang 1 khi chạy bài mới
                
            # Kiểm tra điều kiện biên theo đề bài
            if n < 0 or n > 8:
                error = "Vui lòng nhập n trong khoảng 0 đến 8."
            elif k < 0 or k > n:
                error = "Vui lòng nhập k thỏa mãn 0 <= k <= n."
            else:
                so_luong = so_chinh_hop(n, k)
                full_de_quy = liet_ke_chinh_hop(n, k)
                
                # Phân trang: Chỉ lấy 50 kết quả cho trang hiện tại
                total_pages = (len(full_de_quy) + per_page - 1) // per_page
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page
                ket_qua_de_quy = full_de_quy[start_idx:end_idx]
                
                if k > 0:
                    full_sinh = sinh_ke_tiep_chinh_hop(n, k)
                    ket_qua_sinh = full_sinh[start_idx:end_idx]
                    # Lấy dữ liệu trace (đã được giới hạn bên logic.py)
                    _, trace_data = liet_ke_chinh_hop_co_trace(n, k)
                
                if request.method == 'POST':
                    luu_lich_su(n, k, so_luong)
                    
        except ValueError:
            error = "Dữ liệu nhập vào không hợp lệ."
            
    # Khởi tạo biến total_pages nếu chưa có để tránh lỗi HTML
    if 'total_pages' not in locals():
        total_pages = 1

    # Lấy 5 lần tính toán gần nhất
    db = get_db()
    lich_su = db.execute('SELECT * FROM history ORDER BY id DESC LIMIT 5').fetchall()

    return render_template('index.html', 
                           n=n, k=k, so_luong=so_luong, 
                           ket_qua_de_quy=ket_qua_de_quy,
                           ket_qua_sinh=ket_qua_sinh,
                           trace_data=trace_data,
                           lich_su=lich_su,
                           error=error, da_chay=da_chay,
                           page=page, total_pages=total_pages)

# ==============================================================================
# RESTFUL API (Dành cho Mobile App hoặc bên thứ 3 gọi)
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
    app.run(host='0.0.0.0', port=port, debug=True)