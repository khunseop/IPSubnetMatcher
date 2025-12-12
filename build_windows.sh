#!/bin/bash
# Windows 빌드 스크립트 (WSL 또는 Git Bash에서 사용)

echo "========================================"
echo "IP Network Matcher - Windows 빌드"
echo "========================================"
echo ""

# 가상환경 활성화 (있는 경우)
if [ -f "venv/Scripts/activate" ]; then
    echo "가상환경 활성화 중..."
    source venv/Scripts/activate
fi

# PyInstaller 설치 확인
python -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "PyInstaller 설치 중..."
    pip install pyinstaller
fi

# UPX 확인 (선택사항)
if command -v upx &> /dev/null; then
    echo "UPX 발견됨 - 압축 활성화"
else
    echo ""
    echo "참고: UPX가 설치되지 않았습니다. (선택사항)"
    echo "UPX 설치 시 실행 파일 용량이 더 작아집니다."
    echo "설치 방법: UPX_SETUP.md 파일 참조"
    echo ""
fi

echo ""
echo "빌드 시작..."
echo ""

# 빌드 실행
pyinstaller build_windows.spec --clean

if [ $? -ne 0 ]; then
    echo ""
    echo "빌드 실패!"
    exit 1
fi

echo ""
echo "========================================"
echo "빌드 완료!"
echo "========================================"
echo ""
echo "실행 파일 위치: dist/IPNetworkMatcher.exe"
echo ""

