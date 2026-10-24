from flask import Flask, render_template, request, jsonify, g, Response
import sqlite3
import itertools
import csv
import io
from logic import (so_chinh_hop, liet_ke_chinh_hop, sinh_ke_tiep_chinh_hop, 
                   liet_ke_chinh_hop_co_trace, liet_ke_cat_nhanh, do_hieu_qua, 
                   kiem_tra_tinh_dung, sinh_ke_tiep_chinh_hop_generator,
                   lay_phan_tu_cua_trang)
import os

app = Flask(__name__)
DATABASE = 'history.db'

# ==============================================================================
# QUẢN LÝ DATABASE
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
                       co_rang_buoc INTEGER DEFAULT 0,
                       che_do TEXT DEFAULT 'hoc',
                       thoi_gian TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        db.commit()

if not os.path.exists(DATABASE):
    init_db()

def luu_lich_su(n, k, so_luong, co_rang_buoc, che_do):
    db = get_db()
    try:
        db.execute('ALTER TABLE history ADD COLUMN co_rang_buoc INTEGER DEFAULT 0')
        db.execute('ALTER TABLE history ADD COLUMN che_do TEXT DEFAULT "hoc"')
    except sqlite3.OperationalError:
        pass
        
    db.execute('INSERT INTO history (n, k, so_luong, co_rang_buoc, che_do) VALUES (?, ?, ?, ?, ?)', 
               (n, k, so_luong, 1 if co_rang_buoc else 0, che_do))
    db.commit()

# ==============================================================================
# HÀM TÍNH DẢI PHÂN TRANG THÔNG MINH
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
# LUỒNG XỬ LÝ CHÍNH
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
    
    che_do = request.form.get('che_do') if request.method == 'POST' else request.args.get('che_do', 'hoc')
    co_rang_buoc = (request.form.get('co_rang_buoc') == 'on') if request.method == 'POST' else (request.args.get('co_rang_buoc') == '1')

    if n_str is not None and k_str is not None:
        try:
            n = int(n_str)
            k = int(k_str)
            da_chay = True
            
            if request.method == 'POST':
                page = 1

            # Xác định giới hạn n động
            if co_rang_buoc:
                max_n = 8
            elif che_do == 'dem':
                max_n = 12
            elif che_do == 'hoc':
                max_n = 11
            else:
                max_n = 10

            if n < 0:
                error = "Vui lòng nhập n là số nguyên không âm."
            elif n > max_n:
                error = f"Chế độ hiện tại chỉ hỗ trợ n trong khoảng 0 đến {max_n}."
            elif k < 0 or k > n:
                error = "Vui lòng nhập k thỏa mãn 0 <= k <= n."
            else:
                so_luong = so_chinh_hop(n, k)

                if co_rang_buoc:
                    rang_buoc = {'not_first': 1, 'not_adjacent': (2, 3)}
                    full_de_quy, _ = liet_ke_cat_nhanh(n, k, rang_buoc)
                    so_sanh = do_hieu_qua(n, k, rang_buoc)
                    trace_data = []
                    
                    chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                    full_de_quy = [[chars[v-1] for v in day] for day in full_de_quy]

                    total_pages = max(1, (len(full_de_quy) + per_page - 1) // per_page)
                    start_idx = (page - 1) * per_page
                    end_idx = start_idx + per_page
                    ket_qua_de_quy = full_de_quy[start_idx:end_idx]

                elif che_do == 'hoc':
                    _, trace_data = liet_ke_chinh_hop_co_trace(n, k, max_steps=1000)
                    ket_qua_de_quy = []
                    total_pages = 1
                    if len(trace_data) >= 1000:
                        trace_truncated = True

                elif che_do == 'dem':
                    ket_qua_de_quy = []
                    total_pages = 1

                else:  # che_do == 'liet_ke'
                    # Sử dụng Unranking: Nhảy trực tiếp đến trang cần xem
                    total_pages = max(1, (so_luong + per_page - 1) // per_page)
                    ket_qua_de_quy = lay_phan_tu_cua_trang(n, k, page, per_page)

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

@app.route('/api/verify', methods=['GET'])
def api_verify():
    try:
        n = int(request.args.get('n', 0))
        k = int(request.args.get('k', 0))
        
        if n < 0 or n > 8 or k < 0 or k > n:
            return jsonify({"error": "Tính năng kiểm tra tự động chỉ hỗ trợ n <= 8 để đảm bảo không bị Timeout."}), 400
            
        results = kiem_tra_tinh_dung(n, k)
        all_passed = all(r["status"] for r in results)
        
        return jsonify({
            "all_passed": all_passed,
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============================================================================
# MỞ RỘNG 2: XUẤT CSV BẰNG STREAM (DÙNG CHUẨN csv.writer)
# ==============================================================================
@app.route('/api/export', methods=['GET'])
def api_export():
    try:
        n = int(request.args.get('n', 0))
        k = int(request.args.get('k', 0))
        
        max_n = 10 
        if n < 0 or n > max_n or k < 0 or k > n:
            return jsonify({"error": f"Tham số không hợp lệ. Yêu cầu 0 <= k <= n <= {max_n}"}), 400
            
        def generate_csv():
            # Khởi tạo bộ đệm
            data = io.StringIO()
            # Sử dụng csv.writer để tự động xử lý ngoặc kép/dấu phẩy
            writer = csv.writer(data)
            
            # Ghi header
            writer.writerow(['STT', 'Chỉnh hợp'])
            yield '\ufeff' + data.getvalue() # Thêm BOM UTF-8 cho Excel
            data.seek(0)
            data.truncate(0)
            
            count = 1
            for day in sinh_ke_tiep_chinh_hop_generator(n, k):
                day_str = "[" + ", ".join(map(str, day)) + "]"
                writer.writerow([count, day_str])
                yield data.getvalue()
                
                # Reset bộ đệm cho dòng tiếp theo
                data.seek(0)
                data.truncate(0)
                count += 1
                
        return Response(
            generate_csv(), 
            mimetype='text/csv', 
            headers={'Content-Disposition': f'attachment; filename=chinh_hop_n{n}_k{k}.csv'}
        )
        
    except ValueError:
        return jsonify({"error": "Invalid parameter type."}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)