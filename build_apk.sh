#!/bin/bash

echo "═══════════════════════════════════════════════════════════════"
echo "🚀 بناء تطبيق الإجازات والدوام - APK"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت!"
    echo "✅ ثبّت Python من: https://www.python.org"
    exit 1
fi

# التحقق من Buildozer
if ! pip3 show buildozer &> /dev/null; then
    echo "📦 جاري تثبيت Buildozer..."
    pip3 install buildozer cython kivy flask -q
    echo "✅ تم التثبيت"
    echo ""
fi

# التحقق من Java
if ! command -v java &> /dev/null; then
    echo "⚠️  Java غير مثبت"
    echo "✅ ثبّت Java:"
    echo "   Ubuntu/Debian: sudo apt-get install openjdk-11-jdk"
    echo "   macOS: brew install java"
    echo ""
fi

echo "🔨 جاري بناء التطبيق..."
echo "(قد يستغرق 10-15 دقيقة)"
echo ""

buildozer -u android debug

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "✅ تم البناء بنجاح!"
    echo "📍 الملف: bin/leavemgmt-1.0-debug.apk"
    echo ""
    echo "🎯 الخطوات التالية:"
    echo "1. انسخ الملف من المجلد bin"
    echo "2. نقله إلى هاتفك"
    echo "3. ثبّته عبر تطبيق البحث"
    echo "═══════════════════════════════════════════════════════════════"
else
    echo ""
    echo "❌ حدث خطأ في البناء"
    echo "تحقق من الأخطاء أعلاه"
fi
