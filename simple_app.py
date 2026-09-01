#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق رصيد الاجازات والدوام - نسخة بسيطة بدون Kivy
Simple Version Without Kivy
"""

import sqlite3
from datetime import datetime, timedelta, date
from pathlib import Path

class LeaveDatabase:
    """إدارة قاعدة البيانات"""
    
    def __init__(self, db_path='leave_management.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._initialize_db()
    
    def _initialize_db(self):
        """إنشاء جداول البيانات"""
        # جدول الموظفين
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                hire_date TEXT NOT NULL,
                shift_type TEXT NOT NULL,
                status TEXT DEFAULT 'نشط'
            )
        ''')
        
        # جدول الإجازات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS leave_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                leave_type TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                days REAL NOT NULL,
                status TEXT DEFAULT 'معلق'
            )
        ''')
        
        self.conn.commit()
    
    def get_all_employees(self):
        """الحصول على جميع الموظفين"""
        self.cursor.execute('SELECT * FROM employees')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def add_employee(self, name, position, hire_date, shift_type):
        """إضافة موظف"""
        self.cursor.execute('''
            INSERT INTO employees (name, position, hire_date, shift_type)
            VALUES (?, ?, ?, ?)
        ''', (name, position, hire_date, shift_type))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def close(self):
        """إغلاق قاعدة البيانات"""
        if self.conn:
            self.conn.close()


class SimpleApp:
    """التطبيق البسيط"""
    
    def __init__(self):
        self.db = LeaveDatabase()
    
    def clear_screen(self):
        """مسح الشاشة"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_menu(self):
        """عرض القائمة الرئيسية"""
        self.clear_screen()
        print("=" * 60)
        print("🎯 تطبيق رصيد الاجازات والدوام")
        print("   Leave and Shift Management System")
        print("=" * 60)
        print()
        print("1️⃣  - عرض جميع الموظفين")
        print("2️⃣  - إضافة موظف جديد")
        print("3️⃣  - إضافة بيانات تجريبية")
        print("0️⃣  - خروج")
        print()
        print("=" * 60)
    
    def show_employees(self):
        """عرض الموظفين"""
        print("\n📋 قائمة الموظفين:\n")
        employees = self.db.get_all_employees()
        
        if not employees:
            print("❌ لا توجد موظفين")
        else:
            print(f"{'الرقم':<5} {'الاسم':<20} {'المنصب':<20} {'نوع الدوام':<10}")
            print("-" * 55)
            for emp in employees:
                print(f"{emp['id']:<5} {emp['name']:<20} {emp['position']:<20} {emp['shift_type']:<10}")
        
        input("\n📍 اضغط Enter للعودة...")
    
    def add_employee(self):
        """إضافة موظف"""
        print("\n➕ إضافة موظف جديد\n")
        
        name = input("اسم الموظف: ").strip()
        position = input("المنصب: ").strip()
        hire_date = input("تاريخ التعيين (YYYY-MM-DD): ").strip()
        
        print("\nنوع الدوام:")
        print("1. صباحي")
        print("2. مسائي")
        
        shift_choice = input("اختر (1 أو 2): ").strip()
        shift_type = "صباحي" if shift_choice == "1" else "مسائي"
        
        try:
            emp_id = self.db.add_employee(name, position, hire_date, shift_type)
            print(f"\n✅ تم إضافة الموظف بنجاح! (الرقم: {emp_id})")
        except Exception as e:
            print(f"\n❌ خطأ: {str(e)}")
        
        input("\n📍 اضغط Enter للعودة...")
    
    def add_sample_data(self):
        """إضافة بيانات تجريبية"""
        print("\n📝 جاري إضافة بيانات تجريبية...\n")
        
        sample_employees = [
            ("أحمد محمد", "مهندس", "2020-01-15", "صباحي"),
            ("فاطمة علي", "محاسبة", "2019-05-20", "صباحي"),
            ("عمر حسن", "مدير", "2018-03-10", "صباحي"),
            ("ليلى إبراهيم", "موظفة", "2021-07-25", "مسائي"),
            ("محمود أحمد", "فني", "2020-11-30", "مسائي"),
        ]
        
        for name, position, hire_date, shift_type in sample_employees:
            try:
                self.db.add_employee(name, position, hire_date, shift_type)
                print(f"✅ تم إضافة: {name}")
            except:
                pass
        
        print("\n✅ تم إضافة البيانات التجريبية!")
        input("\n📍 اضغط Enter للعودة...")
    
    def run(self):
        """تشغيل البرنامج"""
        while True:
            self.show_menu()
            choice = input("👇 أدخل اختيارك: ").strip()
            
            if choice == "1":
                self.show_employees()
            elif choice == "2":
                self.add_employee()
            elif choice == "3":
                self.add_sample_data()
            elif choice == "0":
                self.clear_screen()
                print("👋 شكراً لاستخدامك التطبيق!")
                break
            else:
                print("\n❌ اختيار غير صحيح")
                input("\n📍 اضغط Enter للعودة...")
        
        self.db.close()


if __name__ == '__main__':
    app = SimpleApp()
    app.run()
