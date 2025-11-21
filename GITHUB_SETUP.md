# GitHub에 올리는 방법

## 방법 1: 자동 스크립트 사용 (권장)

```bash
./.github_setup.sh
```

스크립트가 다음을 자동으로 수행합니다:
1. Git 초기화 (이미 초기화되어 있으면 스킵)
2. 파일 추가 및 커밋
3. 원격 레포지토리 연결
4. GitHub에 푸시

## 방법 2: 수동 설정

### 1단계: GitHub에서 레포지토리 생성

1. https://github.com/new 접속
2. 레포지토리 이름 입력 (예: `IPSubnetMatcher`)
3. Public 또는 Private 선택
4. **README, .gitignore, license는 추가하지 마세요** (이미 있음)
5. "Create repository" 클릭

### 2단계: 로컬에서 Git 설정

```bash
# Git 초기화 (아직 안 했다면)
git init

# 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit"

# 브랜치 이름을 main으로 설정 (필요시)
git branch -M main

# 원격 레포지토리 연결 (YOUR_USERNAME과 REPO_NAME을 실제 값으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# GitHub에 푸시
git push -u origin main
```

### 예시

```bash
git init
git add .
git commit -m "Initial commit: IP Network Matcher"
git branch -M main
git remote add origin https://github.com/yourusername/IPSubnetMatcher.git
git push -u origin main
```

## 문제 해결

### 인증 오류
GitHub에 푸시할 때 인증이 필요합니다:

**옵션 1: GitHub CLI 사용**
```bash
gh auth login
git push -u origin main
```

**옵션 2: Personal Access Token 사용**
1. GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. "Generate new token" 클릭
3. 권한 선택 (repo)
4. 토큰 복사
5. 푸시 시 비밀번호 대신 토큰 입력

**옵션 3: SSH 키 사용**
```bash
# SSH 키 생성 (없는 경우)
ssh-keygen -t ed25519 -C "your_email@example.com"

# GitHub에 SSH 키 추가
# Settings > SSH and GPG keys > New SSH key
# 생성된 키 복사: cat ~/.ssh/id_ed25519.pub

# 원격 URL을 SSH로 변경
git remote set-url origin git@github.com:YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

### 이미 원격 레포지토리가 있는 경우
```bash
# 기존 원격 확인
git remote -v

# 원격 URL 변경
git remote set-url origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

## 다음 단계

레포지토리가 생성되면:
1. README.md 파일이 자동으로 표시됩니다
2. Issues 탭에서 이슈 관리 가능
3. Releases 탭에서 버전 관리 가능
4. Actions 탭에서 CI/CD 설정 가능

## .gitignore 확인

다음 파일/폴더는 자동으로 제외됩니다:
- `build/`, `dist/` (빌드 파일)
- `__pycache__/`, `*.pyc` (Python 캐시)
- `venv/`, `env/` (가상환경)
- `.DS_Store`, `Thumbs.db` (OS 파일)

