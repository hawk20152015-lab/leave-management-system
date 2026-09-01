#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف البدء الرئيسي لتطبيق رصيد الاجازات والدوام
Main Entry Point
"""

import os
import sys
from pathlib import Path

def clear_screen():
    """مسح شاشة الكونسول"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    """عرض القائمة الرئيسية"""
    clear_screen()
    print("=" * 60)
    print("🎯 تطبيق رصيد الاجازات والدوام")
    print("   Leave and Shift Management System")
    print("=" * 60)
    print()
    print("اختر أحد الخيارات:")
    print()
    print("  1️⃣  - تشغيل التطبيق الرسومي (Kivy/KivyMD)")
    print("  2️⃣  - إضافة بيانات تجريبية")
    print("  3️⃣  - عرض إحصائيات البيانات")
    print("  4️⃣  - تصدير البيانات (تقرير)")
    print("  5️⃣  - النسخ الاحتياطي")
    print("  6️⃣  - الإعدادات")
    print("  7️⃣  - المساعدة")
    print("  0️⃣  - خروج")
    print()
    print("=" * 60)

def run_gui_app():
    """تشغيل التطبيق الرسومي"""
    try:
        print("\n🚀 جاري تشغيل التطبيق...\n")
        from leave_management_app import LeaveManagementApp
        app = LeaveManagementApp()
        app.run()
        
        # بعد انتهاء التطبيق، نعود للقائمة الرئيسية
        print("\n✅ تم إغلاق التطبيق بنجاح")
        print("   جاري العودة للقائمة الرئيسية...")
        input("\n📍 اضغط Enter للمتابعة...")
        
    except ImportError:
        print("❌ خطأ: لم يتم العثور على مكتبات Kivy/KivyMD")
        print("   يرجى تثبيت المتطلبات:")
        print("   $ pip install -r requirements.txt")
        input("\n📍 اضغط Enter للعودة...")
        
    except SystemExit:
        # معالجة خروج Kivy بشكل صحيح
        print("\n✅ تم إغلاق التطبيق بنجاح")
        print("   جاري العودة للقائمة الرئيسية...")
        input("\n📍 اضغط Enter للمتابعة...")
        
    except KeyboardInterrupt:
        # معالجة Ctrl+C
        print("\n⚠️ تم إيقاف التطبيق بواسطة المستخدم")
        print("   جاري العودة للقائمة الرئيسية...")
        input("\n📍 اضغط Enter للمتابعة...")
        
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        input("\n📍 اضغط Enter للعودة...")

def run_sample_data():
    """إضافة بيانات تجريبية"""
    try:
        print("\n📝 جاري إضافة بيانات تجريبية...\n")
        from sample_data import populate_sample_data, print_statistics
        
        db_path = populate_sample_data()
        print_statistics(db_path)
        
        print("\n✅ تم إضافة البيانات بنجاح!")
        print(f"   ملف الاختبار: {db_path}")
        
        input("\n📍 اضغط Enter للعودة...")
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {str(e)}")
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")

def show_statistics():
    """عرض إحصائيات البيانات"""
    try:
        print("\n📊 عرض الإحصائيات\n")
        
        from leave_management_app import LeaveDatabase, LeaveCalculator
        from datetime import datetime
        
        # اختيار قاعدة البيانات
        db_files = list(Path('.').glob('*.db'))
        
        if not db_files:
            print("❌ لا توجد قاعدة بيانات!")
            print("   يرجى إضافة بيانات تجريبية أولاً (الخيار 2)")
            input("\n📍 اضغط Enter للعودة...")
            return
        
        print("📁 قواعد البيانات المتاحة:")
        for i, db_file in enumerate(db_files, 1):
            print(f"  {i}. {db_file.name}")
        
        choice = input("\nاختر رقم قاعدة البيانات: ").strip()
        
        try:
            db_index = int(choice) - 1
            if 0 <= db_index < len(db_files):
                db_path = str(db_files[db_index])
            else:
                print("❌ اختيار غير صحيح")
                return
        except ValueError:
            print("❌ أدخل رقماً صحيحاً")
            return
        
        db = LeaveDatabase(db_path)
        calculator = LeaveCalculator(db)
        
        year = datetime.now().year
        employees = db.get_all_employees()
        
        print(f"\n📈 إحصائيات السنة {year}:\n")
        print(f"{'الاسم':<20} {'الدوام':<10} {'أيام الدوام':<15} {'الرصيد المتبقي':<15}")
        print("-" * 60)
        
        for emp in employees:
            balance = calculator.calculate_annual_leave_balance(emp['id'], year)
            
            total_days = balance['morning_duty_days'] + balance['shift_duty_days']
            remaining = balance['remaining_balance']
            
            print(f"{emp['name']:<20} {balance['shift_type']:<10} {total_days:<15} {remaining:<15}")
        
        db.close()
        
        input("\n📍 اضغط Enter للعودة...")
    
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        input("\n📍 اضغط Enter للعودة...")

def export_data():
    """تصدير البيانات"""
    try:
        print("\n📤 تصدير البيانات\n")
        
        from leave_management_app import LeaveDatabase
        from utils_and_reports import ReportGenerator, DataExporter
        from datetime import datetime
        
        # اختيار قاعدة البيانات
        db_files = list(Path('.').glob('*.db'))
        
        if not db_files:
            print("❌ لا توجد قاعدة بيانات!")
            input("\n📍 اضغط Enter للعودة...")
            return
        
        print("📁 قواعد البيانات المتاحة:")
        for i, db_file in enumerate(db_files, 1):
            print(f"  {i}. {db_file.name}")
        
        choice = input("\nاختر رقم قاعدة البيانات: ").strip()
        
        try:
            db_index = int(choice) - 1
            if 0 <= db_index < len(db_files):
                db_path = str(db_files[db_index])
            else:
                print("❌ اختيار غير صحيح")
                return
        except ValueError:
            print("❌ أدخل رقماً صحيحاً")
            return
        
        db = LeaveDatabase(db_path)
        year = datetime.now().year
        
        print("\nصيغ التصدير المتاحة:")
        print("  1. JSON")
        print("  2. HTML")
        print("  3. CSV")
        
        export_choice = input("\nاختر الصيغة: ").strip()
        
        report = ReportGenerator.generate_department_report(db, year)
        
        if export_choice == "1":
            filename = DataExporter.export_to_json(report)
            print(f"✅ تم التصدير إلى: {filename}")
        
        elif export_choice == "2":
            filename = DataExporter.export_to_html(report)
            print(f"✅ تم التصدير إلى: {filename}")
        
        elif export_choice == "3":
            employees = db.get_all_employees()
            filename = DataExporter.export_to_csv(employees)
            print(f"✅ تم التصدير إلى: {filename}")
        
        else:
            print("❌ اختيار غير صحيح")
        
        db.close()
        
        input("\n📍 اضغط Enter للعودة...")
    
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        input("\n📍 اضغط Enter للعودة...")

def backup_data():
    """النسخ الاحتياطي"""
    try:
        print("\n💾 النسخ الاحتياطي\n")
        
        from utils_and_reports import BackupManager
        
        db_files = list(Path('.').glob('*.db'))
        
        if not db_files:
            print("❌ لا توجد قاعدة بيانات!")
            input("\n📍 اضغط Enter للعودة...")
            return
        
        print("📁 قواعد البيانات المتاحة:")
        for i, db_file in enumerate(db_files, 1):
            print(f"  {i}. {db_file.name}")
        
        choice = input("\nاختر رقم قاعدة البيانات للنسخ الاحتياطي: ").strip()
        
        try:
            db_index = int(choice) - 1
            if 0 <= db_index < len(db_files):
                db_path = str(db_files[db_index])
            else:
                print("❌ اختيار غير صحيح")
                return
        except ValueError:
            print("❌ أدخل رقماً صحيحاً")
            return
        
        backup_path = BackupManager.create_backup(db_path)
        print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
        
        print("\n📋 النسخ الاحتياطية المتاحة:")
        backups = BackupManager.list_backups()
        for backup in backups:
            print(f"  • {backup}")
        
        input("\n📍 اضغط Enter للعودة...")
    
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        input("\n📍 اضغط Enter للعودة...")

def show_help():
    """عرض المساعدة"""
    clear_screen()
    print("=" * 60)
    print("📚 المساعدة والدعم")
    print("=" * 60)
    print()
    print("🔹 الملفات المهمة:")
    print("   - README.md: الدليل الكامل")
    print("   - QUICK_START.md: دليل البدء السريع")
    print()
    print("🔹 المتطلبات:")
    print("   - Python 3.8+")
    print("   - Kivy 2.1.0+")
    print("   - KivyMD 1.1.1+")
    print()
    print("🔹 قاعدة البيانات:")
    print("   - SQLite (مدمجة)")
    print("   - ملف: leave_management.db أو sample_leave_management.db")
    print()
    print("🔹 الأعطال الرسمية المدعومة:")
    print("   - جميع الأعطال الرسمية العراقية (2024-2026)")
    print("   - نهاية الأسبوع (الجمعة والسبت)")
    print()
    print("🔹 الدعم:")
    print("   - راجع ملف README.md للمزيد من المعلومات")
    print()
    print("=" * 60)
    input("\n📍 اضغط Enter للعودة...")

def main():
    """البرنامج الرئيسي"""
    while True:
        show_menu()
        choice = input("\n👇 أدخل اختيارك: ").strip()
        
        if choice == "1":
            run_gui_app()
        
        elif choice == "2":
            run_sample_data()
        
        elif choice == "3":
            show_statistics()
        
        elif choice == "4":
            export_data()
        
        elif choice == "5":
            backup_data()
        
        elif choice == "6":
            clear_screen()
            print("الإعدادات قيد التطوير...")
            input("\n📍 اضغط Enter للعودة...")
        
        elif choice == "7":
            show_help()
        
        elif choice == "0":
            clear_screen()
            print("👋 شكراً لاستخدامك تطبيق رصيد الاجازات والدوام!")
            print()
            sys.exit(0)
        
        else:
            print("\n❌ اختيار غير صحيح! حاول مرة أخرى.")
            input("\n📍 اضغط Enter للعودة...")

if __name__ == '__main__':
    # تطوير وتصميم بواسطة عمر كريم
    # Development and Design by Omar Karim
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 تم إيقاف التطبيق بواسطة المستخدم.")
        sys.exit(0)
    except SystemExit as e:
        # معالجة خروج النظام (يحدث عند إغلاق Kivy)
        if e.code == 0:
            # خروج طبيعي
            pass
        else:
            print(f"\n❌ خطأ في النظام: {str(e)}")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {str(e)}")
        sys.exit(1)
