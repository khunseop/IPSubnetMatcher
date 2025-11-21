"""결과 그리드 모듈 - 컴팩트 버전"""
import customtkinter as ctk
from tkinter import ttk
from typing import List, Dict


class ResultGrid(ctk.CTkFrame):
    """결과 표시 그리드"""
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=8, border_width=1, border_color=("#1f1f2e", "#1f1f2e"), fg_color=("#151520", "#151520"))
        
        # 헤더 영역
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 8))
        
        # 제목 레이블
        title_label = ctk.CTkLabel(
            header_frame,
            text="Results",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left")
        
        # 통계 레이블
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text="0개",
            font=ctk.CTkFont(size=12),
            text_color=("#6b7280", "#9ca3af"),
            anchor="e"
        )
        self.stats_label.pack(side="right")
        
        # Treeview를 위한 프레임
        tree_frame = ctk.CTkFrame(self, corner_radius=6)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 스크롤바 스타일 설정
        style = ttk.Style()
        style.theme_use("clam")
        
        is_dark = ctk.get_appearance_mode() == "dark"
        
        # 다크 모드에 맞게 스타일 설정 (강제 적용)
        if is_dark:
            style.configure("Treeview",
                           background="#1e1e2e",
                           foreground="#e0e0e0",
                           fieldbackground="#1e1e2e",
                           borderwidth=1,
                           font=("Segoe UI", 11),
                           rowheight=26)
            
            style.configure("Treeview.Heading",
                           background="#2d2d44",
                           foreground="#e0e0e0",
                           font=("Segoe UI", 11, "bold"),
                           borderwidth=1,
                           relief="flat",
                           padding=(6, 4))
            
            # 스크롤바도 다크 테마
            style.configure("TScrollbar",
                           background="#2d2d44",
                           troughcolor="#1e1e2e",
                           borderwidth=0,
                           arrowcolor="#e0e0e0",
                           darkcolor="#2d2d44",
                           lightcolor="#2d2d44")
        else:
            style.configure("Treeview",
                           background="#ffffff",
                           foreground="#1a1a2e",
                           fieldbackground="#ffffff",
                           borderwidth=1,
                           font=("Segoe UI", 11),
                           rowheight=26)
            
            style.configure("Treeview.Heading",
                           background="#f3f4f6",
                           foreground="#1a1a2e",
                           font=("Segoe UI", 11, "bold"),
                           borderwidth=1,
                           relief="flat",
                           padding=(6, 4))
        
        style.map("Treeview.Heading",
                 background=[("active", "#3b3b5c" if is_dark else "#e5e7eb")])
        
        style.map("Treeview",
                 background=[("selected", "#3b82f6" if is_dark else "#3b82f6")],
                 foreground=[("selected", "#ffffff" if is_dark else "#ffffff")])
        
        if is_dark:
            style.map("TScrollbar",
                     background=[("active", "#3b3b5c")],
                     arrowcolor=[("active", "#ffffff")])
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(tree_frame, style="TScrollbar")
        scrollbar.pack(side="right", fill="y")
        
        # Treeview
        columns = ("Source", "Type", "Status", "NetworkName", "Location", "CIDR")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15,
            style="Treeview"
        )
        scrollbar.config(command=self.tree.yview)
        
        # 컬럼 설정
        self.tree.heading("Source", text="Source")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Status", text="Status")
        self.tree.heading("NetworkName", text="Network Name")
        self.tree.heading("Location", text="Location")
        self.tree.heading("CIDR", text="CIDR")
        
        # 컬럼 너비 설정
        self.tree.column("Source", width=150, anchor="w")
        self.tree.column("Type", width=70, anchor="center")
        self.tree.column("Status", width=60, anchor="center")
        self.tree.column("NetworkName", width=150, anchor="w")
        self.tree.column("Location", width=120, anchor="w")
        self.tree.column("CIDR", width=150, anchor="w")
        
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        
        # 데이터 저장용
        self.results_data = []
    
    def display_results(self, results: List[Dict]):
        """
        결과를 그리드에 표시
        
        Args:
            results: 매칭 결과 리스트
        """
        # 기존 데이터 삭제
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.results_data = results
        
        # 통계 계산
        total = len(results)
        matched = sum(1 for r in results if r.get('matched', False))
        
        # 통계 업데이트
        if total > 0:
            self.stats_label.configure(text=f"{matched}/{total} 매칭")
        else:
            self.stats_label.configure(text="0개")
        
        # 결과 추가
        for result in results:
            source = result.get('source', '')
            ip_type = result.get('type', '')
            matched = result.get('matched', False)
            network_name = result.get('matched_network_name', '')
            location = result.get('matched_location', '')
            cidr = result.get('matched_cidr', '')
            
            status = "O" if matched else "X"
            
            # 아이템 추가
            item_id = self.tree.insert(
                "",
                "end",
                values=(source, ip_type, status, network_name, location, cidr)
            )
            
            # 색상 태그 설정
            if matched:
                self.tree.item(item_id, tags=("matched",))
            else:
                self.tree.item(item_id, tags=("unmatched",))
        
        # 태그 스타일 설정
        is_dark = ctk.get_appearance_mode() == "dark"
        self.tree.tag_configure("matched", foreground="#10b981", 
                               background="#1a1a2e" if is_dark else "#f0fdf4")
        self.tree.tag_configure("unmatched", foreground="#ef4444", 
                               background="#1a1a2e" if is_dark else "#fef2f2")
    
    def get_results_data(self) -> List[Dict]:
        """결과 데이터 반환"""
        return self.results_data
