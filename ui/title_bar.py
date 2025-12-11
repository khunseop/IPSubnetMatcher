"""커스텀 타이틀 바 모듈 - 미니멀 디자인"""
import customtkinter as ctk


class CustomTitleBar(ctk.CTkFrame):
    """커스텀 타이틀 바 - 미니멀 스타일"""
    
    def __init__(self, parent, root_window, on_close=None):
        """
        Args:
            parent: 부모 위젯
            root_window: 루트 윈도우 (이동용)
            on_close: 닫기 콜백
        """
        super().__init__(parent, height=28, corner_radius=0, fg_color=("#1a1a1a", "#1a1a1a"), border_width=0)
        self.root_window = root_window
        self.on_close = on_close
        
        # 드래그 관련 변수
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.dragging = False
        
        self.setup_title_bar()
    
    def setup_title_bar(self):
        """타이틀 바 구성 - 미니멀 디자인"""
        # 왼쪽: 타이틀 (드래그 가능)
        title_label = ctk.CTkLabel(
            self,
            text="IP Network Matcher",
            font=ctk.CTkFont(size=11),
            anchor="w",
            text_color=("#888888", "#888888")
        )
        title_label.pack(side="left", padx=10, pady=6)
        
        # 드래그 가능한 영역
        title_label.bind("<Button-1>", self.start_drag)
        title_label.bind("<B1-Motion>", self.on_drag)
        title_label.bind("<ButtonRelease-1>", self.stop_drag)
        
        # 오른쪽: 닫기 버튼만
        close_btn = ctk.CTkButton(
            self,
            text="✕",
            command=self.close_window,
            width=22,
            height=22,
            corner_radius=3,
            font=ctk.CTkFont(size=10),
            fg_color="transparent",
            hover_color=("#f87171", "#f87171"),
            text_color=("#888888", "#888888")
        )
        close_btn.pack(side="right", padx=8, pady=3)
        
        # 타이틀 바 전체를 드래그 가능하게
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
    
    def start_drag(self, event):
        """드래그 시작"""
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        self.dragging = True
    
    def on_drag(self, event):
        """드래그 중"""
        if self.dragging:
            dx = event.x_root - self.drag_start_x
            dy = event.y_root - self.drag_start_y
            x = self.root_window.winfo_x() + dx
            y = self.root_window.winfo_y() + dy
            self.root_window.geometry(f"+{x}+{y}")
            self.drag_start_x = event.x_root
            self.drag_start_y = event.y_root
    
    def stop_drag(self, event):
        """드래그 종료"""
        self.dragging = False
    
    def close_window(self):
        """닫기"""
        if self.on_close:
            self.on_close()
        else:
            self.root_window.destroy()

