"""결과 그리드 모듈 - 텍스트 출력 방식"""
import customtkinter as ctk
from typing import List, Dict


class ResultGrid(ctk.CTkFrame):
    """결과 표시 - 텍스트 출력 방식"""
    
    def __init__(self, parent):
        super().__init__(
            parent, 
            corner_radius=8, 
            border_width=1, 
            border_color=("#e5e7eb", "#e5e7eb"),
            fg_color=("#ffffff", "#ffffff")
        )
        
        # 헤더 영역 (컴팩트)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=6, pady=(6, 4))
        
        # Pretendard 폰트 설정
        try:
            title_font = ctk.CTkFont(family="Pretendard", size=14, weight="bold")
            default_font = ctk.CTkFont(family="Pretendard", size=11)
            text_font = ctk.CTkFont(family="Pretendard", size=12)
        except:
            title_font = ctk.CTkFont(size=14, weight="bold")
            default_font = ctk.CTkFont(size=11)
            text_font = ctk.CTkFont(size=12)
        
        # 제목 레이블
        title_label = ctk.CTkLabel(
            header_frame,
            text="Results",
            font=title_font,
            anchor="w",
            text_color=("#111827", "#111827")
        )
        title_label.pack(side="left")
        
        # 통계 레이블 (미니멀)
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text="0개",
            font=default_font,
            text_color=("#6b7280", "#6b7280"),
            anchor="e"
        )
        self.stats_label.pack(side="right")
        
        # 텍스트 출력 영역 (모던 다크)
        try:
            # 코드 폰트는 Consolas 유지하되 Pretendard와 함께 사용
            code_font = ctk.CTkFont(family="Consolas", size=12)
        except:
            code_font = text_font
        
        try:
            self.textbox = ctk.CTkTextbox(
                self,
                font=code_font,
                fg_color=("#ffffff", "#ffffff"),
                text_color=("#111827", "#111827"),
                border_color=("#e5e7eb", "#e5e7eb"),
                border_width=1,
                corner_radius=6,
                wrap="none"
            )
        except:
            self.textbox = ctk.CTkTextbox(
                self,
                font=text_font,
                fg_color=("#ffffff", "#ffffff"),
                text_color=("#111827", "#111827"),
                border_color=("#e5e7eb", "#e5e7eb"),
                border_width=1,
                corner_radius=6,
                wrap="none"
            )
        self.textbox.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        
        # 데이터 저장용
        self.results_data = []
    
    def display_results(self, results: List[Dict]):
        """
        결과를 텍스트로 표시 (애니메이션 효과)
        
        Args:
            results: 매칭 결과 리스트 [{'source': str, 'matched_ips': str}, ...]
        """
        self.results_data = results
        
        # 통계 계산
        total = len(results)
        matched = sum(1 for r in results if r.get('matched_ips', '').strip())
        
        # 통계 업데이트 (미니멀) - 파란색 포인트
        if total > 0:
            new_text = f"{matched}/{total}"
            self.stats_label.configure(text=new_text, text_color=("#3b82f6", "#3b82f6"))
            self.after(200, lambda: self.stats_label.configure(text_color=("#6b7280", "#6b7280")))
        else:
            self.stats_label.configure(text="0개")
        
        # 텍스트 출력 (최적화: 한 번에 삽입)
        self.textbox.delete("1.0", "end")
        
        if not results:
            self.textbox.insert("1.0", "결과가 없습니다.")
            return
        
        # 결과를 텍스트로 포맷팅 (최적화: 리스트 컴프리헨션 사용)
        lines = [
            f"{result.get('source', '')}\t→\t{result.get('matched_ips', '') or '(매칭 없음)'}"
            for result in results
        ]
        
        # 텍스트 삽입 (최적화: 한 번에 삽입)
        text_content = '\n'.join(lines)
        self.textbox.insert("1.0", text_content)
        
        # 스크롤을 맨 위로
        self.textbox.see("1.0")
    
    def get_results_data(self) -> List[Dict]:
        """결과 데이터 반환"""
        return self.results_data
