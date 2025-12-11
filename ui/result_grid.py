"""결과 그리드 모듈 - 텍스트 출력 방식"""
import customtkinter as ctk
from typing import List, Dict


class ResultGrid(ctk.CTkFrame):
    """결과 표시 - 텍스트 출력 방식"""
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=6, border_width=0, fg_color=("#1a1a1a", "#1a1a1a"))
        
        # 헤더 영역 (컴팩트)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=6, pady=(6, 3))
        
        # 제목 레이블
        title_label = ctk.CTkLabel(
            header_frame,
            text="Results",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w",
            text_color=("#e0e0e0", "#e0e0e0")
        )
        title_label.pack(side="left")
        
        # 통계 레이블
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text="0개",
            font=ctk.CTkFont(size=13),
            text_color=("#888888", "#888888"),
            anchor="e"
        )
        self.stats_label.pack(side="right")
        
        # 텍스트 출력 영역 (완전 다크 테마, 큰 글씨)
        font_family = "Consolas"  # Windows에서 멋진 모노스페이스 폰트
        try:
            self.textbox = ctk.CTkTextbox(
                self,
                font=ctk.CTkFont(size=14, family=font_family),
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
                font=ctk.CTkFont(size=14),
                fg_color=("#1a1a1a", "#1a1a1a"),
                text_color=("#d0d0d0", "#d0d0d0"),
                border_color=("#333333", "#333333"),
                border_width=1,
                corner_radius=4,
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
        
        # 통계 업데이트 (애니메이션 효과)
        if total > 0:
            new_text = f"{matched}/{total}"
            # 숫자 변경 시 색상 애니메이션
            self.stats_label.configure(text=new_text, text_color=("#4ade80", "#4ade80"))
            self.after(300, lambda: self.stats_label.configure(text_color=("#888888", "#888888")))
        else:
            self.stats_label.configure(text="0개")
        
        # 텍스트 출력 (페이드 효과)
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
        
        # 텍스트 삽입 (애니메이션 효과)
        text_content = '\n'.join(lines)
        self.textbox.insert("1.0", text_content)
        
        # 스크롤을 맨 위로 (부드러운 전환)
        self.textbox.see("1.0")
    
    def get_results_data(self) -> List[Dict]:
        """결과 데이터 반환"""
        return self.results_data
