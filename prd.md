# PRD: IP Network Matcher & Diff Tool

## 1. 개요 (Overview)
본 애플리케이션은 사용자가 입력한 **조회 대상 IP(Source)**들이 사전에 정의된 **네트워크 대역(Reference)**에 속하는지 여부를 즉시 판별하는 도구이다. 텍스트 복사/붙여넣기와 파일 업로드를 모두 지원하며, 'Diff 툴'처럼 좌우 대조가 가능한 UI를 제공하여 직관적인 분석과 엑셀 리포팅을 목표로 한다.

## 2. 사용자 흐름 (User Flow)
1.  **Input (Source):** 사용자가 조회하고 싶은 IP 리스트를 왼쪽 패널에 붙여넣거나 텍스트 파일을 로드한다.
2.  **Reference (Network):** 비교할 기준이 되는 네트워크 대역을 오른쪽 패널에 붙여넣거나 엑셀 파일을 로드한다.
3.  **Action:** [분석(Analyze)] 버튼을 클릭한다.
4.  **Process:** 프로그램이 다양한 입력 포맷(Single, CIDR, Range)을 파싱하여 매칭 여부를 검사한다.
5.  **Output:** 하단 그리드에 결과가 즉시 표시되며, 필요시 [엑셀로 저장] 버튼으로 파일을 다운로드한다.

## 3. 핵심 기능 요구사항 (Functional Requirements)

### 3.1 데이터 입력 (Input Processing)
* **지원 방식:**
    * **직접 입력 (Copy & Paste):** 텍스트 영역(Text Area)에 데이터 붙여넣기 지원.
    * **파일 로드:** `.txt` (단순 리스트), `.xlsx` (엑셀 테이블) 지원.
* **지원 포맷 (Source & Reference 공통):**
    1.  **Single IP:** `192.168.1.1`
    2.  **CIDR:** `192.168.1.0/24`
    3.  **IP Range:** `192.168.1.1-192.168.1.50` (하이픈 포맷)
* **전처리 로직:**
    * 입력된 Range나 CIDR은 내부적으로 IP Set 혹은 Network Object로 정규화하여 비교 준비.
    * 공백(Trim), 빈 줄 자동 제거.

### 3.2 매칭 로직 (Matching Engine)
* **N:M 매칭:** 다수의 Source가 다수의 Reference 중 어디에 속하는지 검사.
* **포함 관계 판단:**
    * Source가 Single IP인 경우: Reference 대역에 포함(Included)되는지 확인.
    * Source가 CIDR/Range인 경우: Reference 대역과 **겹치는지(Overlap)** 혹은 **완전 포함(Contained)**되는지 확인.
* **우선순위:** 하나의 Source가 여러 Reference 대역에 걸칠 경우, 가장 구체적인(Prefix가 긴) 대역 혹은 리스트 상단 대역을 매칭(옵션).

### 3.3 결과 표시 (Output & Visualization)
* **즉시 확인 (Live Grid):**
    * UI 하단에 테이블(Treeview) 형태로 결과 출력.
    * 컬럼 구성: `Source(원본)`, `Type(형식)`, `매칭 상태(O/X)`, `매칭된 네트워크명`, `매칭된 CIDR`
* **시각적 구분:** 매칭 성공 시 녹색 텍스트, 실패 시 적색/회색 텍스트 등으로 구분.
* **통계 요약:** 상단에 "총 00건 중 00건 매칭 성공" 요약 표시.

### 3.4 리포팅 (Reporting)
* **엑셀 내보내기:** 현재 그리드에 표시된 결과를 `.xlsx` 파일로 저장.
* 원본 데이터 형태를 유지하며 분석 결과 컬럼 추가.

## 4. UI/UX 요구사항 (UI Specifications)

### 4.1 레이아웃 (Diff Style Layout)
* **Split Pane (상단):** 좌측 [Source Input] vs 우측 [Reference Input]
    * 각 패널은 "직접 입력 탭"과 "파일 로드 탭" 혹은 혼합형 UI를 가짐.
* **Control Bar (중단):** [분석 시작], [초기화] 버튼 위치.
* **Result Grid (하단):** 분석 결과 리스트 표시 영역.

### 4.2 인터랙션
* 엑셀 파일 로드 시, 헤더(컬럼)를 선택할 수 있는 팝업 또는 드롭다운 제공 (이전 기능 계승).
* 분석 중 UI 멈춤 방지 (비동기 처리 및 Progress Bar).

## 5. 기술 스택 및 제약사항 (Technical Stack)
* **Language:** Python 3.x
* **GUI Library:** `CustomTkinter` (모던 UI)
* **Data Processing:** `pandas`, `ipaddress` (필수: Range 포맷 파싱 로직 추가 구현 필요)
* **Performance:** 수만 건의 IP 비교 시 속도 저하 방지를 위해 `Interval Tree` 또는 `Radix Tree` 알고리즘 고려 (혹은 단순 반복문 최적화).
