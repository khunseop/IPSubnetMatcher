"""입력 패널 모듈 - 심플 텍스트 입력"""
import customtkinter as ctk
from typing import Callable, Optional
import re


class InputPanel(ctk.CTkFrame):
    """Source/Reference 입력 패널 - 텍스트 입력만"""
    
    def __init__(self, parent, title: str, is_reference: bool = False, on_data_change: Optional[Callable] = None):
        """
        Args:
            parent: 부모 위젯
            title: 패널 제목
            is_reference: Reference 패널 여부
            on_data_change: 데이터 변경 시 호출할 콜백 함수
        """
        super().__init__(parent, corner_radius=6, border_width=0, fg_color=("#1a1a1a", "#1a1a1a"))
        self.is_reference = is_reference
        self.on_data_change = on_data_change
        self._update_job = None  # debounce용
        
        # 헤더 영역
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=8, pady=(8, 4))
        
        # 제목 레이블
        self.title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
            text_color=("#e0e0e0", "#e0e0e0")
        )
        self.title_label.pack(side="left")
        
        # 개수 표시 레이블
        self.count_label = ctk.CTkLabel(
            header_frame,
            text="0개",
            font=ctk.CTkFont(size=12),
            text_color=("#888888", "#888888"),
            anchor="e"
        )
        self.count_label.pack(side="right")
        
        # 초기화 버튼만 (간단하게)
        self.clear_btn = ctk.CTkButton(
            header_frame,
            text="초기화",
            command=self.clear_data,
            font=ctk.CTkFont(size=11),
            height=26,
            width=60,
            corner_radius=3,
            fg_color=("#333333", "#333333"),
            hover_color=("#444444", "#444444"),
            text_color=("#e0e0e0", "#e0e0e0")
        )
        self.clear_btn.pack(side="right", padx=(8, 0))
        
        # 텍스트 입력 영역 (완전 다크 테마, 큰 글씨)
        # Windows에서 잘 보이는 폰트: Consolas, Courier New, 'Courier New'
        font_family = "Consolas"  # Windows에서 멋진 모노스페이스 폰트
        try:
            self.textbox = ctk.CTkTextbox(
                self,
                font=ctk.CTkFont(size=12, family=font_family),
                fg_color=("#1a1a1a", "#1a1a1a"),
                text_color=("#d0d0d0", "#d0d0d0"),
                border_color=("#333333", "#333333"),
                border_width=1,
                corner_radius=4,
                wrap="none"
            )
        except:
            # 폰트가 없을 경우 기본 폰트 사용
            self.textbox = ctk.CTkTextbox(
                self,
                font=ctk.CTkFont(size=12),
                fg_color=("#1a1a1a", "#1a1a1a"),
                text_color=("#d0d0d0", "#d0d0d0"),
                border_color=("#333333", "#333333"),
                border_width=1,
                corner_radius=4,
                wrap="none"
            )
        self.textbox.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        # 텍스트 변경 감지 (debounce 적용)
        self.textbox.bind("<KeyRelease>", self.on_text_change)
        self.textbox.bind("<Button-1>", self.on_text_change)
        
        # 안내 텍스트
        placeholder = "IP 주소를 입력하세요.\n개행 또는 콤마(,)로 구분할 수 있습니다."
        self.textbox.insert("1.0", placeholder)
        self.textbox.configure(state="normal")
    
    def on_text_change(self, event=None):
        """텍스트 변경 이벤트 (debounce 적용)"""
        # 기존 예약된 업데이트 취소
        if self._update_job is not None:
            self.after_cancel(self._update_job)
        
        # 300ms 후에 업데이트 실행 (debounce)
        self._update_job = self.after(300, self._do_update)
    
    def _do_update(self):
        """실제 업데이트 수행"""
        self.update_count()
        if self.on_data_change:
            self.on_data_change()
        self._update_job = None
    
    def update_count(self):
        """입력 개수 업데이트 (콤마/개행 기준)"""
        content = self.get_text_content().strip()
        if not content:
            count = 0
        else:
            # 콤마와 개행 모두로 분리하여 개수 계산
            items = re.split(r'[,\n]+', content)
            count = sum(1 for item in items if item.strip())
        self.count_label.configure(text=f"{count}개")
    
    def clear_data(self):
        """데이터 초기화"""
        self.textbox.delete("1.0", "end")
        self.update_count()
        if self.on_data_change:
            self.on_data_change()
    
    def get_text_content(self) -> str:
        """입력된 텍스트 내용 반환"""
        return self.textbox.get("1.0", "end-1c")
