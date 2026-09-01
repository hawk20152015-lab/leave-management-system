@echo off
chcp 65001 >nul
echo ═══════════════════════════════════════════════════════════════
echo 🚀 بناء تطبيق الإجازات والدوام - APK
echo ═══════════════════════════════════════════════════════════════
echo.

REM التحقق من Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت!
    echo ✅ حمّل Python من: https://www.python.org
    pause
    exit /b 1
)

REM التحقق من Buildozer
pip show buildozer >nul 2>&1
if errorlevel 1 (
    echo 📦 جاري تثبيت Buildozer...
    pip install buildozer cython kivy flask -q
    echo ✅ تم التثبيت
    echo.
)

REM التحقق من Java
java -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Java غير مثبت أو لم يُضف للمتغيرات
    echo ✅ حمّل Java من: https://www.oracle.com/java/technologies/downloads/
    echo.
)

echo 🔨 جاري بناء التطبيق...
echo (قد يستغرق 10-15 دقيقة)
echo.

buildozer -u android debug

if errorlevel 0 (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo ✅ تم البناء بنجاح!
    echo 📍 الملف: bin\leavemgmt-1.0-debug.apk
    echo.
    echo 🎯 الخطوات التالية:
    echo 1. انسخ الملف من المجلد bin
    echo 2. نقله إلى هاتفك
    echo 3. ثبّته عبر تطبيق البحث
    echo ═══════════════════════════════════════════════════════════════
) else (
    echo.
    echo ❌ حدث خطأ في البناء
    echo تحقق من الأخطاء أعلاه
)

pause
