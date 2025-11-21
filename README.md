# IP Network Matcher

네트워크 대역 매칭 분석 도구 - IP 주소가 특정 네트워크 대역에 속하는지 확인하는 GUI 애플리케이션

## 주요 기능

- **3열 레이아웃**: Source, Reference, Results를 한 화면에서 확인
- **편집 가능한 그리드**: 한 줄씩 입력하고 수정 가능한 그리드 형태
- **엑셀 파일 지원**: Reference 데이터를 엑셀 파일로 로드 (레벨 4 데이터 자동 필터링)
- **다양한 IP 포맷 지원**: Single IP, CIDR, IP Range (하이픈 포맷)
- **실시간 매칭**: 입력 즉시 분석 및 결과 표시
- **엑셀 내보내기**: 분석 결과를 엑셀 파일로 저장
- **미니멀 다크 UI**: 커스텀 타이틀 바와 글래스모피즘 효과

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
1. **Source Input**: 조회할 IP 주소를 입력 (한 줄에 하나씩)
2. **Reference Input**: 비교할 네트워크 대역을 입력하거나 엑셀 파일 로드
3. **분석 시작**: 버튼 클릭하여 매칭 분석 수행
4. **결과 확인**: Results 패널에서 매칭 결과 확인
5. **엑셀 저장**: 필요시 결과를 엑셀 파일로 저장

### 엑셀 파일 형식 (Reference)
- 3열(C열)부터 데이터 시작
- 필수 컬럼: "네트워크ID", "객체명", "네트워크명", "구분", "레벨", "추가속성", "위치"
- 레벨이 '4'인 행만 자동으로 필터링되어 사용됨
- 네트워크명 컬럼에 IP 정보 (Single/CIDR/Range) 포함

### 지원 포맷
- **Single IP**: `192.168.1.1`
- **CIDR**: `192.168.1.0/24`
- **IP Range**: `192.168.1.1-192.168.1.50`

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
├── core/                   # 핵심 로직
│   ├── parser.py          # IP 파싱
│   ├── matcher.py         # 매칭 엔진
│   └── excel_handler.py   # 엑셀 처리
├── ui/                     # UI 모듈
│   ├── main_window.py     # 메인 윈도우
│   ├── input_panel.py     # 입력 패널
│   ├── result_grid.py     # 결과 그리드
│   └── title_bar.py       # 커스텀 타이틀 바
└── utils/                  # 유틸리티
    └── ip_utils.py         # IP 관련 유틸리티
```

## 기술 스택

- **Python 3.x**
- **CustomTkinter**: 모던 GUI 프레임워크
- **pandas**: 데이터 처리
- **openpyxl**: 엑셀 파일 처리
- **ipaddress**: IP 주소 처리

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트 환영합니다!

