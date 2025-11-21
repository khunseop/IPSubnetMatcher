#!/bin/bash
# GitHub 레포지토리 설정 스크립트

echo "========================================"
echo "GitHub 레포지토리 설정"
echo "========================================"
echo ""

# Git 초기화 확인
if [ ! -d ".git" ]; then
    echo "Git 초기화 중..."
    git init
fi

# 현재 브랜치 확인
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

echo "현재 브랜치: $CURRENT_BRANCH"
echo ""

# 파일 추가
echo "파일 추가 중..."
git add .

# 첫 커밋
echo ""
echo "커밋 메시지를 입력하세요 (기본: Initial commit):"
read -r COMMIT_MSG
COMMIT_MSG=${COMMIT_MSG:-"Initial commit"}

git commit -m "$COMMIT_MSG"

echo ""
echo "========================================"
echo "다음 단계:"
echo "========================================"
echo ""
echo "1. GitHub에서 새 레포지토리 생성:"
echo "   https://github.com/new"
echo ""
echo "2. 레포지토리 이름을 입력하세요:"
read -r REPO_NAME
REPO_NAME=${REPO_NAME:-"IPSubnetMatcher"}

echo ""
echo "3. GitHub 사용자명을 입력하세요:"
read -r GITHUB_USER

echo ""
echo "원격 레포지토리 연결 중..."
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null || \
git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo ""
echo "브랜치 이름 설정 (기본: main):"
read -r BRANCH_NAME
BRANCH_NAME=${BRANCH_NAME:-"main"}

# 브랜치 이름 변경 (필요시)
if [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
    git branch -M "$BRANCH_NAME"
fi

echo ""
echo "GitHub에 푸시하시겠습니까? (y/n)"
read -r PUSH_CONFIRM

if [ "$PUSH_CONFIRM" = "y" ] || [ "$PUSH_CONFIRM" = "Y" ]; then
    echo ""
    echo "푸시 중..."
    git push -u origin "$BRANCH_NAME"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "========================================"
        echo "완료!"
        echo "========================================"
        echo ""
        echo "레포지토리 URL: https://github.com/$GITHUB_USER/$REPO_NAME"
    else
        echo ""
        echo "푸시 실패. GitHub 인증이 필요할 수 있습니다."
        echo "GitHub CLI 또는 Personal Access Token을 사용하세요."
    fi
else
    echo ""
    echo "수동으로 푸시하려면 다음 명령어를 실행하세요:"
    echo "  git push -u origin $BRANCH_NAME"
fi

