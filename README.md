# IP Network Matcher

네트워크 대역 매칭 분석 도구 - IP 주소가 특정 네트워크 대역에 속하는지 확인하는 가볍고 빠른 GUI 애플리케이션

## 주요 기능

- **3열 레이아웃**: Source, Reference, Results를 한 화면에서 확인
- **텍스트 입력**: 콤마(,) 또는 개행으로 구분하여 IP 입력
- **다양한 IP 포맷 지원**: Single IP, CIDR, IP Range (하이픈 포맷)
- **고성능 매칭**: 3만 개 이상의 대역도 빠르게 처리
- **비동기 처리**: 분석 중에도 UI가 멈추지 않음
- **엑셀 내보내기**: 분석 결과를 깔끔한 서식의 엑셀 파일로 저장
- **미니멀 다크 UI**: 심플하고 가벼운 디자인

## 설치 방법

### 요구사항
- Python 3.8 이상
- pip

### 설치
```bash
# 저장소 클론
git clone https://github.com/YOUR_USERNAME/IPSubnetMatcher.git
cd IPSubnetMatcher

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

## 사용 방법

### 실행
```bash
python main.py
```

### 사용법
1. **Source Input**: 조회할 IP 주소를 입력 (콤마 또는 개행으로 구분)
2. **Reference Input**: 비교할 네트워크 대역을 입력 (콤마 또는 개행으로 구분)
3. **분석**: 버튼 클릭하여 매칭 분석 수행
4. **결과 확인**: Results 패널에서 매칭 결과 확인 (대상 IP → 매칭된 IP)
5. **엑셀 저장**: 필요시 결과를 엑셀 파일로 저장

### 입력 형식
IP 주소는 다음 형식으로 입력할 수 있으며, 콤마(`,`) 또는 개행(`\n`)으로 구분합니다:

```
192.168.1.1, 10.0.0.1, 172.16.0.0/24
192.168.1.1-192.168.1.50
```

또는

```
192.168.1.1
10.0.0.1
172.16.0.0/24
192.168.1.1-192.168.1.50
```

### 지원 포맷
- **Single IP**: `192.168.1.1`
- **CIDR**: `192.168.1.0/24`
- **IP Range**: `192.168.1.1-192.168.1.50`

### 결과 형식
- **대상 IP**: 입력한 Source IP
- **매칭된 IP**: 매칭된 Reference IP들 (여러 개일 경우 콤마로 구분)

## Windows 실행 파일 빌드

```bash
# 배치 파일 실행
build_windows.bat

# 또는 수동 빌드
pip install pyinstaller
pyinstaller build_windows.spec --clean
```

빌드된 실행 파일: `dist/IPNetworkMatcher.exe`

## 프로젝트 구조

```
IPSubnetMatcher/
├── main.py                 # 메인 진입점
├── requirements.txt        # 패키지 의존성
├── build_windows.spec      # PyInstaller 빌드 설정
├── build_windows.bat       # Windows 빌드 스크립트
├── build_windows.sh        # Windows 빌드 스크립트 (WSL/Git Bash)
├── core/                   # 핵심 로직
│   ├── parser.py          # IP 파싱 (배치 처리, 비동기 지원)
│   └── matcher.py         # 매칭 엔진 (고성능 최적화)
├── ui/                     # UI 모듈
│   ├── main_window.py     # 메인 윈도우
│   ├── input_panel.py     # 입력 패널
│   ├── result_grid.py     # 결과 표시
│   └── title_bar.py       # 커스텀 타이틀 바
└── utils/                  # 유틸리티
    └── ip_utils.py         # IP 관련 유틸리티
```

## 기술 스택

- **Python 3.x**
- **CustomTkinter**: 모던 GUI 프레임워크
- **openpyxl**: 엑셀 파일 저장
- **ipaddress**: IP 주소 처리 (Python 표준 라이브러리)

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트 환영합니다!

