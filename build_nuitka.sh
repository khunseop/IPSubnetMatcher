#!/bin/bash
# Nuitka 빌드 스크립트 - macOS/Linux용
# UPX 압축 포함

echo "========================================"
echo "IP Network Matcher - Nuitka 빌드 (UPX 포함)"
echo "========================================"
echo ""

# 가상환경 활성화 (있는 경우)
if [ -f "venv/bin/activate" ]; then
    echo "가상환경 활성화 중..."
    source venv/bin/activate
fi

# Nuitka 설치 확인
python -c "import nuitka" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Nuitka 설치 중..."
    pip install nuitka
fi

# UPX 설치 확인 (선택사항)
if command -v upx &> /dev/null; then
    echo "UPX 발견됨 - 압축 활성화"
    UPX_OPTION="--plugin-enable=upx --upx-binary=upx --upx-exclude=python*.so"
else
    echo ""
    echo "경고: UPX가 설치되지 않았습니다."
    echo "UPX 없이 빌드합니다. (용량이 더 클 수 있습니다)"
    echo "UPX 설치: brew install upx (macOS) 또는 apt-get install upx (Linux)"
    echo ""
    UPX_OPTION=""
fi

echo ""
echo "빌드 시작..."
echo ""

# Nuitka 빌드 실행
python -m nuitka --standalone --onefile \
    --remove-output \
    --lto=yes \
    $UPX_OPTION \
    --include-package=customtkinter \
    --include-package=openpyxl \
    --include-data-dir=customtkinter/assets=customtkinter/assets \
    main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "빌드 실패!"
    echo ""
    echo "UPX 오류가 발생한 경우, UPX 없이 빌드해보세요:"
    echo "python -m nuitka --standalone --onefile --include-package=customtkinter --include-package=openpyxl main.py"
    exit 1
fi

echo ""
echo "========================================"
echo "빌드 완료!"
echo "========================================"
echo ""
echo "실행 파일 위치: main.dist/main"
echo ""

