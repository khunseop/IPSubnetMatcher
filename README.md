# IP Network Matcher

네트워크 대역 매칭 분석 도구 - IP 주소가 특정 네트워크 대역에 속하는지 확인하는 가볍고 빠른 GUI 애플리케이션

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 📋 목차

- [주요 기능](#주요-기능)
- [스크린샷](#스크린샷)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [빌드 및 배포](#빌드-및-배포)
- [프로젝트 구조](#프로젝트-구조)
- [기술 스택](#기술-스택)
- [성능](#성능)
- [문제 해결](#문제-해결)
- [라이선스](#라이선스)
- [기여](#기여)

## ✨ 주요 기능

- **3열 레이아웃**: Source, Reference, Results를 한 화면에서 확인
- **텍스트 입력**: 콤마(,) 또는 개행으로 구분하여 IP 입력
- **다양한 IP 포맷 지원**: 
  - Single IP: `192.168.1.1`
  - CIDR: `192.168.1.0/24`
  - IP Range: `192.168.1.1-192.168.1.50` (하이픈 포맷)
- **고성능 매칭**: 3만 개 이상의 대역도 빠르게 처리
- **비동기 처리**: 분석 중에도 UI가 멈추지 않음
- **엑셀 내보내기**: 분석 결과를 깔끔한 서식의 엑셀 파일로 저장
- **미니멀 UI**: 심플하고 가벼운 디자인

## 📸 스크린샷

애플리케이션은 3열 레이아웃으로 구성되어 있습니다:
- **좌측**: Source 입력 패널
- **중앙**: Reference 입력 패널  
- **우측**: 매칭 결과 표시

## 🚀 설치 방법

### 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자)

### 소스 코드에서 설치

```bash
# 저장소 클론
git clone https://github.com/YOUR_USERNAME/IPSubnetMatcher.git
cd IPSubnetMatcher

# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 실행

```bash
python main.py
```

## 📖 사용 방법

### 기본 사용법

1. **Source 입력**: 좌측 패널에 조회할 IP 주소를 입력합니다
   - 콤마(`,`) 또는 개행(`\n`)으로 구분하여 여러 IP 입력 가능
   
2. **Reference 입력**: 중앙 패널에 비교할 네트워크 대역을 입력합니다
   - 동일하게 콤마 또는 개행으로 구분하여 입력 가능

3. **분석 실행**: 상단의 "분석" 버튼을 클릭합니다
   - 분석 중에는 진행 상황이 하단 상태 바에 표시됩니다
   - 대용량 데이터도 비동기 처리로 UI가 멈추지 않습니다

4. **결과 확인**: 우측 Results 패널에서 매칭 결과를 확인합니다
   - 매칭된 IP는 "매칭된 IP" 컬럼에 표시됩니다
   - 여러 대역에 매칭된 경우 콤마로 구분하여 표시됩니다

5. **엑셀 저장**: 필요시 "저장" 버튼을 클릭하여 결과를 엑셀 파일로 저장합니다

### 입력 형식 예시

#### 콤마로 구분
```
192.168.1.1, 10.0.0.1, 172.16.0.0/24, 192.168.1.1-192.168.1.50
```

#### 개행으로 구분
```
192.168.1.1
10.0.0.1
172.16.0.0/24
192.168.1.1-192.168.1.50
```

#### 혼합 형식
```
192.168.1.1, 10.0.0.1
172.16.0.0/24
192.168.1.1-192.168.1.50
```

### 지원 포맷 상세

| 포맷 | 예시 | 설명 |
|------|------|------|
| **Single IP** | `192.168.1.1` | 단일 IP 주소 |
| **CIDR** | `192.168.1.0/24` | CIDR 표기법 네트워크 대역 |
| **IP Range** | `192.168.1.1-192.168.1.50` | 하이픈으로 구분된 IP 범위 |

### 결과 형식

결과는 다음 형식으로 표시됩니다:

| 대상 IP | 매칭된 IP |
|---------|-----------|
| `192.168.1.1` | `192.168.1.0/24, 10.0.0.0/8` |
| `10.0.0.5` | `10.0.0.0/8` |
| `172.16.0.1` | (비어있음 - 매칭 없음) |

## 🔨 빌드 및 배포

### Windows 실행 파일 빌드

#### 방법 1: 배치 파일 사용 (권장)

```bash
# Windows
build_windows.bat

# 또는 Git Bash/WSL
bash build_windows.sh
```

#### 방법 2: 수동 빌드

```bash
# PyInstaller 설치 (이미 설치되어 있으면 생략)
pip install pyinstaller

# 빌드 실행
pyinstaller build_windows.spec --clean
```

빌드된 실행 파일은 `dist/IPNetworkMatcher.exe`에 생성됩니다.

### 빌드 옵션

`build_windows.spec` 파일에서 다음을 설정할 수 있습니다:
- 아이콘 파일 경로
- 실행 파일 이름
- 포함할 데이터 파일
- 콘솔 창 표시 여부

### 배포 패키징

배포 시 다음 파일들을 포함하세요:
- `dist/IPNetworkMatcher.exe` (Windows)
- `README.md` (사용 설명서)
- `LICENSE` (라이선스)

## 📁 프로젝트 구조

```
IPSubnetMatcher/
├── main.py                 # 메인 진입점
├── requirements.txt        # 패키지 의존성
├── build_windows.spec      # PyInstaller 빌드 설정
├── build_windows.bat       # Windows 빌드 스크립트
├── build_windows.sh        # Windows 빌드 스크립트 (WSL/Git Bash)
├── icons8-비교-50.ico      # 애플리케이션 아이콘
├── LICENSE                 # MIT 라이선스
├── README.md              # 프로젝트 문서
├── core/                   # 핵심 로직
│   ├── __init__.py
│   ├── parser.py          # IP 파싱 (배치 처리, 비동기 지원)
│   └── matcher.py         # 매칭 엔진 (고성능 최적화)
├── ui/                     # UI 모듈
│   ├── __init__.py
│   ├── main_window.py     # 메인 윈도우
│   ├── input_panel.py     # 입력 패널
│   └── result_grid.py     # 결과 표시
└── utils/                  # 유틸리티
    ├── __init__.py
    └── ip_utils.py         # IP 관련 유틸리티
```

## 🛠 기술 스택

- **Python 3.8+**: 프로그래밍 언어
- **CustomTkinter**: 모던 GUI 프레임워크
- **openpyxl**: 엑셀 파일 읽기/쓰기
- **ipaddress**: IP 주소 처리 (Python 표준 라이브러리)
- **PyInstaller**: 실행 파일 빌드

## ⚡ 성능

- **대용량 처리**: 3만 개 이상의 IP 대역도 빠르게 처리
- **최적화된 알고리즘**: Network prefix 길이별 그룹화 및 정수 변환으로 빠른 비교
- **비동기 처리**: UI 블로킹 없이 백그라운드에서 분석 수행
- **배치 처리**: 대량 데이터를 효율적으로 처리

### 성능 벤치마크 (참고)

| 데이터 크기 | 처리 시간 (예상) |
|------------|-----------------|
| 1,000개 | < 1초 |
| 10,000개 | < 5초 |
| 30,000개 | < 15초 |

*실제 성능은 하드웨어 및 데이터 특성에 따라 다를 수 있습니다.*

## 🐛 문제 해결

### 일반적인 문제

#### 1. 모듈을 찾을 수 없음 (ModuleNotFoundError)

```bash
# 가상환경이 활성화되어 있는지 확인
# requirements.txt의 패키지가 모두 설치되었는지 확인
pip install -r requirements.txt
```

#### 2. 아이콘이 표시되지 않음

- `icons8-비교-50.ico` 파일이 프로젝트 루트에 있는지 확인
- macOS/Linux에서는 ICO 파일 지원이 제한적일 수 있습니다

#### 3. 빌드 실패

- PyInstaller가 최신 버전인지 확인: `pip install --upgrade pyinstaller`
- 빌드 전에 이전 빌드 파일 정리: `pyinstaller build_windows.spec --clean`

#### 4. 실행 파일이 너무 큼

- `build_windows.spec`에서 불필요한 모듈 제외
- UPX 압축 사용 (기본 활성화됨)

### 지원

문제가 발생하면 다음을 확인하세요:
1. Python 버전이 3.8 이상인지 확인
2. 모든 의존성 패키지가 설치되었는지 확인
3. GitHub Issues에 문제 보고

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🤝 기여

기여를 환영합니다! 다음 방법으로 기여할 수 있습니다:

1. **이슈 보고**: 버그나 기능 제안은 GitHub Issues에 등록해주세요
2. **풀 리퀘스트**: 개선사항이 있으면 Pull Request를 보내주세요
3. **문서 개선**: 문서의 오타나 개선사항을 발견하면 알려주세요

### 기여 가이드라인

- 코드 스타일은 기존 코드와 일치하도록 유지해주세요
- 새로운 기능 추가 시 테스트를 포함해주세요
- 커밋 메시지는 명확하고 간결하게 작성해주세요

## 📝 변경 이력

### 버전 1.0.0
- 초기 릴리스
- 기본 IP 매칭 기능
- 엑셀 내보내기 기능
- Windows 실행 파일 빌드 지원

---

**만든 이**: [Your Name]  
**이메일**: [your.email@example.com]  
**GitHub**: [https://github.com/YOUR_USERNAME/IPSubnetMatcher]
