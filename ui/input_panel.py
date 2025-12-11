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
        super().__init__(
            parent, 
            corner_radius=6, 
            border_width=1, 
            border_color=("#e5e7eb", "#e5e7eb"),
            fg_color=("#ffffff", "#ffffff")
        )
        self.is_reference = is_reference
        self.on_data_change = on_data_change
        self._update_job = None  # debounce용
        
        # 헤더 영역 (컴팩트)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=8, pady=(8, 4))
        
        # 제목 레이블
        self.title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
            text_color=("#111827", "#111827")
        )
        self.title_label.pack(side="left")
        
        # 초기화 버튼 (컴팩트)
        self.clear_btn = ctk.CTkButton(
            header_frame,
            text="초기화",
            command=self.clear_data,
            font=ctk.CTkFont(size=10),
            height=22,
            width=50,
            corner_radius=4,
            fg_color="transparent",
            hover_color=("#f3f4f6", "#f3f4f6"),
            text_color=("#6b7280", "#6b7280"),
            border_width=0
        )
        self.clear_btn.pack(side="right")
        
        # 개수 표시 레이블 (미니멀)
        self.count_label = ctk.CTkLabel(
            header_frame,
            text="0개",
            font=ctk.CTkFont(size=10),
            text_color=("#6b7280", "#6b7280"),
            anchor="e"
        )
        self.count_label.pack(side="right", padx=(0, 6))
        
        # 텍스트 입력 영역 (미니멀)
        font_family = "Consolas"
        try:
            self.textbox = ctk.CTkTextbox(
                self,
                font=ctk.CTkFont(size=11, family=font_family),
                fg_color=("#ffffff", "#ffffff"),
                text_color=("#111827", "#111827"),
                border_color=("#e5e7eb", "#e5e7eb"),
                border_width=1,
                corner_radius=4,
                wrap="none"
            )
        except:
            self.textbox = ctk.CTkTextbox(
                self,
                font=ctk.CTkFont(size=11),
                fg_color=("#ffffff", "#ffffff"),
                text_color=("#111827", "#111827"),
                border_color=("#e5e7eb", "#e5e7eb"),
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
        """입력 개수 업데이트 (콤마/개행 기준, 애니메이션 효과)"""
        content = self.get_text_content().strip()
        if not content:
            count = 0
        else:
            # 콤마와 개행 모두로 분리하여 개수 계산
            items = re.split(r'[,\n]+', content)
            count = sum(1 for item in items if item.strip())
        
        # 숫자 변경 시 애니메이션 효과
        current_text = self.count_label.cget("text")
        new_text = f"{count}개"
        
        if current_text != new_text:
            # 간단한 색상 변경
            self.count_label.configure(text=new_text, text_color=("#2563eb", "#2563eb"))
            self.after(200, lambda: self.count_label.configure(text_color=("#6b7280", "#6b7280")))
        else:
            self.count_label.configure(text=new_text)
    
    def clear_data(self):
        """데이터 초기화"""
        self.textbox.delete("1.0", "end")
        self.update_count()
        if self.on_data_change:
            self.on_data_change()
    
    def get_text_content(self) -> str:
        """입력된 텍스트 내용 반환"""
        return self.textbox.get("1.0", "end-1c")
