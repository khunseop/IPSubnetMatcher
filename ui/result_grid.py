"""결과 그리드 모듈 - 텍스트 출력 방식"""
import customtkinter as ctk
from typing import List, Dict


class ResultGrid(ctk.CTkFrame):
    """결과 표시 - 텍스트 출력 방식"""
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=6, border_width=0, fg_color=("#1a1a1a", "#1a1a1a"))
        
        # 헤더 영역
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=8, pady=(8, 4))
        
        # 제목 레이블
        title_label = ctk.CTkLabel(
            header_frame,
            text="Results",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
            text_color=("#e0e0e0", "#e0e0e0")
        )
        title_label.pack(side="left")
        
        # 통계 레이블
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text="0개",
            font=ctk.CTkFont(size=11),
            text_color=("#888888", "#888888"),
            anchor="e"
        )
        self.stats_label.pack(side="right")
        
        # 텍스트 출력 영역 (완전 다크 테마)
        self.textbox = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(size=10, family="Monaco"),
            fg_color=("#1a1a1a", "#1a1a1a"),
            text_color=("#d0d0d0", "#d0d0d0"),
            border_color=("#333333", "#333333"),
            border_width=1,
            corner_radius=4,
            wrap="none"
        )
        self.textbox.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        # 데이터 저장용
        self.results_data = []
    
    def display_results(self, results: List[Dict]):
        """
        결과를 텍스트로 표시
        
        Args:
            results: 매칭 결과 리스트 [{'source': str, 'matched_ips': str}, ...]
        """
        self.results_data = results
        
        # 통계 계산
        total = len(results)
        matched = sum(1 for r in results if r.get('matched_ips', '').strip())
        
        # 통계 업데이트
        if total > 0:
            self.stats_label.configure(text=f"{matched}/{total}")
        else:
            self.stats_label.configure(text="0개")
        
        # 텍스트 출력
        self.textbox.delete("1.0", "end")
        
        if not results:
            self.textbox.insert("1.0", "결과가 없습니다.")
            return
        
        # 결과를 텍스트로 포맷팅
        lines = []
        for result in results:
            source = result.get('source', '')
            matched_ips = result.get('matched_ips', '')
            
            if matched_ips.strip():
                lines.append(f"{source}\t→\t{matched_ips}")
            else:
                lines.append(f"{source}\t→\t(매칭 없음)")
        
        # 텍스트 삽입
        text_content = '\n'.join(lines)
        self.textbox.insert("1.0", text_content)
    
    def get_results_data(self) -> List[Dict]:
        """결과 데이터 반환"""
        return self.results_data
