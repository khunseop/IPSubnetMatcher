"""메인 윈도우 모듈 - 3열 레이아웃"""
import customtkinter as ctk
from tkinter import filedialog
import threading
from core.parser import IPParser
from core.excel_handler import ExcelHandler
from core.matcher import Matcher
from ui.input_panel import InputPanel
from ui.result_grid import ResultGrid
from ui.title_bar import CustomTitleBar
import pandas as pd
import platform


class MainWindow:
    """메인 윈도우 클래스"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("IP Network Matcher")
        
        # 윈도우 커스터마이징
        self.setup_window()
        
        # 데이터 저장
        self.source_data = []
        self.reference_data = []
        
        self.setup_ui()
    
    def setup_window(self):
        """윈도우 설정 및 커스터마이징"""
        # 기본 타이틀 바 제거 (커스텀 타이틀 바 사용)
        self.root.overrideredirect(True)
        
        # 윈도우 크기
        self.root.geometry("1400x700")
        self.root.minsize(1200, 600)
        
        # 투명도 효과 (다크 테마 유지)
        self.root.attributes("-alpha", 0.97)
        
        # 윈도우 중앙 배치
        self.center_window()
        
        # 배경색 설정 (다크 테마)
        self.root.configure(bg="#0f0f1e")
    
    def center_window(self):
        """윈도우를 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """UI 구성 - 3열 레이아웃"""
        # 커스텀 타이틀 바
        self.title_bar = CustomTitleBar(
            self.root,
            self.root,
            on_close=self.on_close
        )
        self.title_bar.pack(fill="x", side="top")
        
        # 메인 컨테이너 (미니멀 다크 테마)
        main_container = ctk.CTkFrame(
            self.root,
            fg_color=("#0f0f1e", "#0f0f1e"),
            corner_radius=0
        )
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 내부 컨테이너
        inner_container = ctk.CTkFrame(main_container, fg_color="transparent")
        inner_container.pack(fill="both", expand=True, padx=16, pady=16)
        
        # 컨트롤 버튼 영역 (미니멀 디자인)
        control_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        control_frame.pack(fill="x", pady=(0, 12))
        
        # 버튼 그룹 (오른쪽 정렬)
        button_group = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_group.pack(side="right")
        
        self.analyze_btn = ctk.CTkButton(
            button_group,
            text="분석 시작",
            command=self.start_analysis,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=36,
            width=100,
            corner_radius=6,
            fg_color=("#3b82f6", "#2563eb"),
            hover_color=("#2563eb", "#1d4ed8")
        )
        self.analyze_btn.pack(side="left", padx=(0, 6))
        
        self.export_btn = ctk.CTkButton(
            button_group,
            text="엑셀 저장",
            command=self.export_to_excel,
            font=ctk.CTkFont(size=13),
            height=36,
            width=100,
            corner_radius=6,
            fg_color=("#10b981", "#059669"),
            hover_color=("#059669", "#047857"),
            state="disabled"
        )
        self.export_btn.pack(side="left", padx=(0, 6))
        
        self.reset_btn = ctk.CTkButton(
            button_group,
            text="초기화",
            command=self.reset_all,
            font=ctk.CTkFont(size=13),
            height=36,
            width=80,
            corner_radius=6,
            fg_color=("#6b7280", "#4b5563"),
            hover_color=("#4b5563", "#374151")
        )
        self.reset_btn.pack(side="left")
        
        # 3열 레이아웃
        columns_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        columns_frame.pack(fill="both", expand=True)
        
        # 좌측: Source 패널
        self.source_panel = InputPanel(
            columns_frame,
            "Source Input",
            is_reference=False,
            on_data_change=self.on_data_change
        )
        self.source_panel.pack(side="left", fill="both", expand=True, padx=(0, 6))
        
        # 중앙: Reference 패널
        self.reference_panel = InputPanel(
            columns_frame,
            "Reference Input",
            is_reference=True,
            on_data_change=self.on_data_change
        )
        self.reference_panel.pack(side="left", fill="both", expand=True, padx=(6, 6))
        
        # 우측: 결과 패널
        self.result_grid = ResultGrid(columns_frame)
        self.result_grid.pack(side="left", fill="both", expand=True, padx=(6, 0))
        
        # 하단 상태 바
        status_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.progress_label = ctk.CTkLabel(
            status_frame,
            text="준비됨",
            font=ctk.CTkFont(size=12),
            text_color=("#6b7280", "#9ca3af")
        )
        self.progress_label.pack(side="left")
    
    def on_data_change(self):
        """데이터 변경 이벤트 핸들러"""
        # 패널이 아직 생성되지 않았을 수 있으므로 확인
        if not hasattr(self, 'source_panel') or not hasattr(self, 'reference_panel'):
            return
        
        source_text = self.source_panel.get_text_content().strip()
        reference_text = self.reference_panel.get_text_content().strip()
        reference_file = self.reference_panel.get_file_path()
        
        if (source_text or self.source_panel.get_file_path()) and (reference_text or reference_file):
            self.analyze_btn.configure(state="normal")
        else:
            self.analyze_btn.configure(state="disabled")
    
    def start_analysis(self):
        """분석 시작"""
        self.analyze_btn.configure(state="disabled", text="분석 중...")
        self.progress_label.configure(text="분석 중...", text_color=("#3b82f6", "#60a5fa"))
        
        # 별도 스레드에서 실행 (UI 멈춤 방지)
        thread = threading.Thread(target=self.perform_analysis)
        thread.daemon = True
        thread.start()
    
    def perform_analysis(self):
        """실제 분석 수행"""
        try:
            # Source 데이터 파싱
            source_file = self.source_panel.get_file_path()
            if source_file:
                self.source_data = IPParser.parse_file(source_file)
            else:
                source_text = self.source_panel.get_text_content()
                self.source_data = IPParser.parse_text_input(source_text)
            
            # Reference 데이터 파싱
            reference_file = self.reference_panel.get_file_path()
            if reference_file and reference_file.endswith('.xlsx'):
                self.reference_data = ExcelHandler.load_reference_excel(reference_file)
            else:
                reference_text = self.reference_panel.get_text_content()
                self.reference_data = []
                if reference_text.strip():
                    parsed_refs = IPParser.parse_text_input(reference_text)
                    for ref in parsed_refs:
                        self.reference_data.append({
                            'network_name': ref['original'],
                            'location': '',
                            'parsed': ref['parsed'],
                            'type': ref['type']
                        })
            
            # 매칭 수행
            results = Matcher.match(self.source_data, self.reference_data)
            
            # UI 업데이트 (메인 스레드에서 실행)
            self.root.after(0, self.update_results, results)
            
        except Exception as e:
            error_msg = f"분석 오류: {str(e)}"
            print(error_msg)
            self.root.after(0, self.show_error, error_msg)
    
    def update_results(self, results):
        """결과 업데이트"""
        self.result_grid.display_results(results)
        matched_count = sum(1 for r in results if r.get('matched', False))
        total_count = len(results)
        self.progress_label.configure(
            text=f"분석 완료: {matched_count}/{total_count} 매칭",
            text_color=("#10b981", "#34d399")
        )
        self.analyze_btn.configure(state="normal", text="분석 시작")
        self.export_btn.configure(state="normal")
    
    def show_error(self, error_msg):
        """오류 메시지 표시"""
        self.progress_label.configure(
            text=f"오류: {error_msg[:50]}",
            text_color=("#ef4444", "#f87171")
        )
        self.analyze_btn.configure(state="normal", text="분석 시작")
    
    def export_to_excel(self):
        """엑셀로 내보내기"""
        results = self.result_grid.get_results_data()
        if not results:
            return
        
        file_path = filedialog.asksaveasfilename(
            title="엑셀 파일로 저장",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                df = pd.DataFrame([{
                    'Source(원본)': r.get('source', ''),
                    'Type(형식)': r.get('type', ''),
                    '매칭 상태': 'O' if r.get('matched', False) else 'X',
                    '매칭된 네트워크명': r.get('matched_network_name', ''),
                    '매칭된 위치': r.get('matched_location', ''),
                    '매칭된 CIDR/대역': r.get('matched_cidr', '')
                } for r in results])
                
                df.to_excel(file_path, index=False, engine='openpyxl')
                file_name = file_path.split('/')[-1]
                self.progress_label.configure(
                    text=f"저장 완료: {file_name}",
                    text_color=("#10b981", "#34d399")
                )
            except Exception as e:
                error_msg = f"저장 오류: {str(e)}"
                print(error_msg)
                self.progress_label.configure(
                    text=f"오류: {error_msg[:50]}",
                    text_color=("#ef4444", "#f87171")
                )
    
    def reset_all(self):
        """전체 초기화"""
        self.source_panel.clear_data()
        self.reference_panel.clear_data()
        self.result_grid.display_results([])
        self.progress_label.configure(text="준비됨", text_color=("#6b7280", "#9ca3af"))
        self.export_btn.configure(state="disabled")
        self.source_data = []
        self.reference_data = []
    
    def on_close(self):
        """윈도우 닫기"""
        self.root.destroy()
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()
