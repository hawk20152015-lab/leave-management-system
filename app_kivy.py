#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق الإجازات والدوام - نسخة Kivy للـ APK
"""

import sqlite3
from threading import Thread
from flask import Flask, render_template_string, request, jsonify
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.webview import WebView
from kivy.core.window import Window
import os

# إعدادات النافذة
Window.size = (1080, 1920)

# إنشاء تطبيق Flask
app_flask = Flask(__name__)
DB_PATH = 'leave_management.db'

def init_db():
    """إنشاء قاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS employees')
    cursor.execute('DROP TABLE IF EXISTS leaves')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            hire_date TEXT NOT NULL,
            shift_type TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            shift_duration TEXT NOT NULL,
            backup_id INTEGER,
            status TEXT DEFAULT 'نشط'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'معلق',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    ''')
    
    sample_data = [
        ("أحمد محمد", "مهندس", "2020-01-15", "صباحي", "07:00", "15:00", "دوام يومي", None),
        ("فاطمة علي", "محاسبة", "2019-05-20", "صباحي", "08:00", "16:00", "دوام يومي", None),
        ("عمر حسن", "مدير", "2018-03-10", "صباحي", "07:30", "15:30", "دوام يومي", None),
        ("ليلى إبراهيم", "موظفة", "2021-07-25", "مسائي", "15:00", "23:00", "3 أيام/أسبوع", None),
        ("محمود أحمد", "فني", "2020-11-30", "مسائي", "14:00", "22:00", "أسبوع", None),
    ]
    
    for name, position, hire_date, shift_type, start_time, end_time, duration, backup_id in sample_data:
        cursor.execute('''
            INSERT INTO employees (name, position, hire_date, shift_type, start_time, end_time, shift_duration, backup_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, position, hire_date, shift_type, start_time, end_time, duration, backup_id))
    
    cursor.execute('UPDATE employees SET backup_id = 5 WHERE id = 4')
    cursor.execute('UPDATE employees SET backup_id = 4 WHERE id = 5')
    
    conn.commit()
    conn.close()

def get_employees():
    """الحصول على جميع الموظفين"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return employees

def get_employee(emp_id):
    """الحصول على موظف واحد"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE id = ?', (emp_id,))
    employee = cursor.fetchone()
    conn.close()
    return dict(employee) if employee else None

def get_leaves():
    """الحصول على جميع الإجازات"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT l.*, e.name as employee_name
        FROM leaves l
        JOIN employees e ON l.employee_id = e.id
        ORDER BY l.start_date DESC
    ''')
    leaves = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return leaves

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إدارة الإجازات والدوام</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 10px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .tabs {
            display: flex;
            border-bottom: 2px solid #eee;
            flex-wrap: wrap;
            overflow-x: auto;
        }
        
        .tab-button {
            flex: 1;
            min-width: 100px;
            padding: 12px;
            border: none;
            background: white;
            color: #333;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        
        .tab-button:hover {
            background: #f5f5f5;
        }
        
        .tab-button.active {
            background: #667eea;
            color: white;
        }
        
        .tab-content {
            display: none;
            padding: 20px;
        }
        
        .tab-content.active {
            display: block;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 12px;
        }
        
        table th {
            background: #667eea;
            color: white;
            padding: 10px;
            text-align: right;
            font-weight: bold;
        }
        
        table td {
            padding: 8px 10px;
            border-bottom: 1px solid #eee;
        }
        
        table tr:hover {
            background: #f9f9f9;
        }
        
        .action-buttons {
            display: flex;
            gap: 3px;
        }
        
        .btn-small {
            padding: 4px 8px;
            font-size: 11px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            font-weight: bold;
        }
        
        .btn-edit {
            background: #17a2b8;
            color: white;
        }
        
        .btn-delete {
            background: #dc3545;
            color: white;
        }
        
        .form-group {
            margin-bottom: 12px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 4px;
            font-weight: bold;
            color: #333;
            font-size: 13px;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 13px;
            font-family: 'Arial', sans-serif;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        
        button.btn {
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            width: 100%;
        }
        
        .alert {
            padding: 12px;
            margin-bottom: 15px;
            border-radius: 4px;
            font-size: 12px;
        }
        
        .alert-info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        .shift-badge {
            display: inline-block;
            padding: 3px 6px;
            border-radius: 15px;
            font-size: 11px;
            font-weight: bold;
        }
        
        .shift-morning {
            background: #fff3cd;
            color: #856404;
        }
        
        .shift-evening {
            background: #d1ecf1;
            color: #0c5460;
        }
        
        .footer {
            background: #333;
            color: #999;
            text-align: center;
            padding: 15px;
            border-top: 1px solid #555;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 إدارة الإجازات والدوام</h1>
            <p>نظام الموظفين والدوام الرسمي</p>
        </div>
        
        <div class="tabs">
            <button class="tab-button active" onclick="showTab('employees')">👥 الموظفين</button>
            <button class="tab-button" onclick="showTab('leaves')">📋 الإجازات</button>
            <button class="tab-button" onclick="showTab('add')">➕ إضافة</button>
        </div>
        
        <!-- تبويب الموظفين -->
        <div id="employees" class="tab-content active">
            <h2>👥 قائمة الموظفين</h2>
            <table id="employees-table">
                <thead>
                    <tr>
                        <th>الرقم</th>
                        <th>الاسم</th>
                        <th>المنصب</th>
                        <th>النوع</th>
                        <th>الوقت</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>
        </div>
        
        <!-- تبويب الإجازات -->
        <div id="leaves" class="tab-content">
            <h2>📋 الإجازات</h2>
            <button class="btn" onclick="showAddLeaveModal()" style="margin-bottom: 15px;">➕ إضافة إجازة</button>
            <table id="leaves-table">
                <thead>
                    <tr>
                        <th>الموظف</th>
                        <th>النوع</th>
                        <th>من</th>
                        <th>إلى</th>
                        <th>الحالة</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>
        </div>
        
        <!-- تبويب الإضافة -->
        <div id="add" class="tab-content">
            <h2>➕ إضافة موظف</h2>
            <form id="addEmployeeForm">
                <div class="form-group">
                    <label>الاسم *</label>
                    <input type="text" id="name" required>
                </div>
                
                <div class="form-group">
                    <label>المنصب *</label>
                    <input type="text" id="position" required>
                </div>
                
                <div class="form-group">
                    <label>نوع الدوام *</label>
                    <select id="shift_type" required>
                        <option value="">-- اختر --</option>
                        <option value="صباحي">صباحي</option>
                        <option value="مسائي">مسائي</option>
                    </select>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label>الصعود *</label>
                        <input type="time" id="start_time" required>
                    </div>
                    <div class="form-group">
                        <label>النزول *</label>
                        <input type="time" id="end_time" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>المدة *</label>
                    <input type="text" id="shift_duration" required>
                </div>
                
                <button type="submit" class="btn">✅ إضافة</button>
            </form>
            <div id="form-message"></div>
        </div>
        
        <div class="footer">
            <p>📱 تطوير و برمجة: <strong>عمر كريم</strong></p>
            <p>© 2026 جميع الحقوق محفوظة</p>
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            loadEmployees();
            loadLeaves();
        });
        
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(e => e.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(e => e.classList.remove('active'));
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        function loadEmployees() {
            fetch('/api/employees')
                .then(r => r.json())
                .then(data => {
                    const table = document.querySelector('#employees-table tbody');
                    table.innerHTML = '';
                    
                    data.forEach(emp => {
                        const badge = emp.shift_type === 'صباحي' 
                            ? '<span class="shift-badge shift-morning">☀️</span>'
                            : '<span class="shift-badge shift-evening">🌙</span>';
                        
                        const row = `
                            <tr>
                                <td>${emp.id}</td>
                                <td>${emp.name}</td>
                                <td>${emp.position}</td>
                                <td>${badge}</td>
                                <td>${emp.start_time} - ${emp.end_time}</td>
                            </tr>
                        `;
                        table.innerHTML += row;
                    });
                });
        }
        
        function loadLeaves() {
            fetch('/api/leaves')
                .then(r => r.json())
                .then(data => {
                    const table = document.querySelector('#leaves-table tbody');
                    table.innerHTML = '';
                    
                    data.forEach(leave => {
                        const row = `
                            <tr>
                                <td>${leave.employee_name}</td>
                                <td>${leave.leave_type}</td>
                                <td>${leave.start_date}</td>
                                <td>${leave.end_date}</td>
                                <td>${leave.status}</td>
                            </tr>
                        `;
                        table.innerHTML += row;
                    });
                });
        }
        
        function showAddLeaveModal() {
            const reason = prompt('اكتب سبب الإجازة:');
            if (reason) alert('تم إضافة الإجازة: ' + reason);
        }
        
        document.getElementById('addEmployeeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('✅ تم إضافة الموظف!');
            document.getElementById('addEmployeeForm').reset();
        });
    </script>
</body>
</html>
'''

# Routes Flask
@app_flask.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app_flask.route('/api/employees')
def api_employees():
    return jsonify(get_employees())

@app_flask.route('/api/leaves')
def api_leaves():
    return jsonify(get_leaves())

@app_flask.route('/api/add-employee', methods=['POST'])
def api_add_employee():
    try:
        data = request.json
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employees (name, position, hire_date, shift_type, start_time, end_time, shift_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['position'], '2024-01-01', 
              data['shift_type'], data['start_time'], data['end_time'], data['shift_duration']))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# تطبيق Kivy
class LeaveApp(App):
    def build(self):
        # شغل Flask في thread منفصل
        flask_thread = Thread(target=self.run_flask, daemon=True)
        flask_thread.start()
        
        # إنشاء layout Kivy
        layout = BoxLayout(orientation='vertical')
        
        # عرض الويب
        webview = WebView(url='http://127.0.0.1:5000/')
        layout.add_widget(webview)
        
        return layout
    
    def run_flask(self):
        init_db()
        app_flask.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    LeaveApp().run()
