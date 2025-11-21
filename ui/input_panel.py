"""입력 패널 모듈 - 편집 가능한 그리드 형태"""
import customtkinter as ctk
from tkinter import filedialog, ttk
from typing import Callable, Optional, List
import tkinter as tk


class EditableTreeview:
    """편집 가능한 Treeview 래퍼 클래스"""
    
    def __init__(self, tree, column, on_value_changed=None):
        self.tree = tree
        self.column = column
        self.entry = None
        self.edit_item = None
        self.edit_column = None
        self.on_value_changed = on_value_changed
        
        # 더블클릭 이벤트 바인딩
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-1>", self.on_click)
    
    def on_click(self, event):
        """클릭 시 편집 중인 Entry 제거"""
        if self.entry:
            self.finish_edit()
    
    def on_double_click(self, event):
        """더블클릭 시 편집 시작"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            
            if item and column:
                self.start_edit(item, column)
    
    def start_edit(self, item, column):
        """편집 시작"""
        # 기존 편집 종료
        if self.entry:
            self.finish_edit()
        
        # 컬럼 인덱스 가져오기
        column_index = int(column.replace('#', '')) - 1
        
        # 현재 값 가져오기
        values = list(self.tree.item(item, 'values'))
        if column_index < len(values):
            current_value = values[column_index]
        else:
            current_value = ""
        
        # 셀 위치 가져오기
        bbox = self.tree.bbox(item, column)
        if not bbox:
            return
        
        x, y, width, height = bbox
        
        # Entry 생성 (width와 height는 생성자에서 지정)
        self.entry = ctk.CTkEntry(
            self.tree,
            font=ctk.CTkFont(size=11, family="Consolas"),
            width=width,
            height=max(height - 2, 20)
        )
        self.entry.insert(0, current_value)
        self.entry.place(x=x, y=y)
        self.entry.focus()
        self.entry.select_range(0, "end")
        
        # 이벤트 바인딩
        self.entry.bind("<Return>", lambda e: self.finish_edit())
        self.entry.bind("<Escape>", lambda e: self.cancel_edit())
        self.entry.bind("<FocusOut>", lambda e: self.finish_edit())
        
        self.edit_item = item
        self.edit_column = column_index
    
    def finish_edit(self):
        """편집 완료"""
        if self.entry and self.edit_item is not None:
            new_value = self.entry.get()
            
            # Treeview 값 업데이트
            values = list(self.tree.item(self.edit_item, 'values'))
            if self.edit_column < len(values):
                old_value = values[self.edit_column]
                values[self.edit_column] = new_value
            else:
                # 값이 없으면 추가
                old_value = ""
                while len(values) <= self.edit_column:
                    values.append("")
                values[self.edit_column] = new_value
            
            self.tree.item(self.edit_item, values=values)
            
            # 값이 변경되었으면 콜백 호출
            if old_value != new_value and self.on_value_changed:
                self.on_value_changed()
            
            # Entry 제거
            self.entry.destroy()
            self.entry = None
            self.edit_item = None
            self.edit_column = None
    
    def cancel_edit(self):
        """편집 취소"""
        if self.entry:
            self.entry.destroy()
            self.entry = None
            self.edit_item = None
            self.edit_column = None


class InputPanel(ctk.CTkFrame):
    """Source/Reference 입력 패널 - 편집 가능한 그리드"""
    
    def __init__(self, parent, title: str, is_reference: bool = False, on_data_change: Optional[Callable] = None):
        """
        Args:
            parent: 부모 위젯
            title: 패널 제목
            is_reference: Reference 패널 여부 (엑셀 파일 지원)
            on_data_change: 데이터 변경 시 호출할 콜백 함수
        """
        super().__init__(parent, corner_radius=8, border_width=1, border_color=("#1f1f2e", "#1f1f2e"), fg_color=("#151520", "#151520"))
        self.is_reference = is_reference
        self.on_data_change = on_data_change
        self.current_file_path = None
        
        # 헤더 영역
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 8))
        
        # 제목 레이블
        self.title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self.title_label.pack(side="left")
        
        # 개수 표시 레이블
        self.count_label = ctk.CTkLabel(
            header_frame,
            text="0개",
            font=ctk.CTkFont(size=12),
            text_color=("#6b7280", "#9ca3af"),
            anchor="e"
        )
        self.count_label.pack(side="right")
        
        # 버튼 프레임
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        # 파일 로드 버튼
        self.load_file_btn = ctk.CTkButton(
            button_frame,
            text="파일 로드",
            command=self.load_file,
            font=ctk.CTkFont(size=12),
            height=28,
            width=90,
            corner_radius=6,
            fg_color=("#6366f1", "#4f46e5"),
            hover_color=("#4f46e5", "#4338ca")
        )
        self.load_file_btn.pack(side="left", padx=(0, 6))
        
        # 추가 버튼
        self.add_btn = ctk.CTkButton(
            button_frame,
            text="추가",
            command=self.add_row,
            font=ctk.CTkFont(size=12),
            height=28,
            width=70,
            corner_radius=6,
            fg_color=("#10b981", "#059669"),
            hover_color=("#059669", "#047857")
        )
        self.add_btn.pack(side="left", padx=(0, 6))
        
        # 삭제 버튼
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="삭제",
            command=self.delete_selected,
            font=ctk.CTkFont(size=12),
            height=28,
            width=70,
            corner_radius=6,
            fg_color=("#ef4444", "#dc2626"),
            hover_color=("#dc2626", "#b91c1c")
        )
        self.delete_btn.pack(side="left", padx=(0, 6))
        
        # 초기화 버튼
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="초기화",
            command=self.clear_data,
            font=ctk.CTkFont(size=12),
            height=28,
            width=70,
            corner_radius=6,
            fg_color=("#6b7280", "#4b5563"),
            hover_color=("#4b5563", "#374151")
        )
        self.clear_btn.pack(side="left")
        
        # Treeview를 위한 프레임
        tree_frame = ctk.CTkFrame(self, corner_radius=6)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 스크롤바 스타일 설정
        style = ttk.Style()
        style.theme_use("clam")
        
        is_dark = ctk.get_appearance_mode() == "dark"
        
        # 기본 Treeview 스타일 수정 (다크 모드에 맞게 강제 적용)
        if is_dark:
            # 다크 테마 강제 적용
            style.configure("Treeview",
                           background="#1e1e2e",
                           foreground="#e0e0e0",
                           fieldbackground="#1e1e2e",
                           borderwidth=1,
                           font=("Consolas", 11),
                           rowheight=28)
            
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
                           font=("Consolas", 11),
                           rowheight=28)
            
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
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Value",),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15,
            selectmode="browse"
        )
        scrollbar.config(command=self.tree.yview)
        
        # 컬럼 설정
        self.tree.heading("Value", text="IP 주소 또는 CIDR")
        self.tree.column("Value", width=300, anchor="w")
        
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        
        # 편집 가능하게 설정
        self.editable = EditableTreeview(
            self.tree, 
            "Value",
            on_value_changed=self.on_value_changed
        )
        
        # 값 변경 감지
        self.tree.bind("<<TreeviewSelect>>", self.on_selection_change)
        
        # 붙여넣기 기능 개선 (여러 방법 지원)
        # Treeview에 바인딩
        self.tree.bind("<Control-v>", self.on_paste)
        self.tree.bind("<Control-V>", self.on_paste)  # 대문자도 지원
        self.tree.bind("<Shift-Insert>", self.on_paste)  # Shift+Insert도 지원
        self.tree.bind("<Button-1>", lambda e: self.tree.focus_set())
        
        # 패널 전체에도 바인딩 (포커스가 없어도 작동)
        self.scrollable_frame.bind("<Control-v>", lambda e: self.on_paste(e))
        self.scrollable_frame.bind("<Control-V>", lambda e: self.on_paste(e))
        self.scrollable_frame.bind("<Shift-Insert>", lambda e: self.on_paste(e))
        
        # 초기 행 하나 추가
        self.add_row(skip_callback=True)
    
    def on_paste(self, event=None):
        """붙여넣기 이벤트 처리 - 개선된 버전"""
        try:
            # Treeview에 포커스 설정
            self.tree.focus_set()
            
            # 클립보드에서 데이터 가져오기 (여러 방법 시도)
            clipboard_text = None
            
            # 방법 1: Tkinter 클립보드
            try:
                clipboard_text = self.tree.clipboard_get()
            except tk.TclError:
                pass
            
            # 방법 2: 시스템 클립보드 (pyperclip 사용 시도)
            if not clipboard_text:
                try:
                    import pyperclip
                    clipboard_text = pyperclip.paste()
                except ImportError:
                    pass
                except Exception:
                    pass
            
            # 방법 3: 직접 클립보드 접근 (Windows/Mac/Linux)
            if not clipboard_text:
                try:
                    root = self.tree.winfo_toplevel()
                    clipboard_text = root.clipboard_get()
                except tk.TclError:
                    pass
            
            if clipboard_text:
                # 다양한 줄바꿈 문자 처리 (\r\n, \n, \r)
                clipboard_text = clipboard_text.replace('\r\n', '\n').replace('\r', '\n')
                
                # 줄 단위로 분리
                lines = clipboard_text.split('\n')
                
                # 빈 줄 제거 및 공백 처리
                processed_lines = []
                for line in lines:
                    line = line.strip()
                    # 탭 문자를 공백으로 변환 (선택사항)
                    line = line.replace('\t', ' ')
                    if line:  # 빈 줄이 아닌 경우만 추가
                        processed_lines.append(line)
                
                if processed_lines:
                    # 선택된 행이 있으면 그 위치부터, 없으면 마지막에 추가
                    selected = self.tree.selection()
                    if selected:
                        # 선택된 행 다음에 추가
                        insert_after = selected[0]
                        for line in processed_lines:
                            new_item = self.tree.insert(insert_after, "end", values=(line,))
                            insert_after = new_item
                    else:
                        # 마지막에 추가
                        for line in processed_lines:
                            self.add_row(line, skip_callback=True)
                    
                    self.update_count()
                    if self.on_data_change:
                        self.on_data_change()
                    
                    # 성공 메시지 (선택사항)
                    # print(f"{len(processed_lines)}개 항목이 추가되었습니다.")
            
            if event:
                return "break"  # 기본 붙여넣기 동작 방지
                
        except tk.TclError as e:
            # 클립보드가 비어있거나 텍스트가 아닌 경우
            print(f"클립보드 접근 오류: {e}")
        except Exception as e:
            print(f"붙여넣기 오류: {e}")
            import traceback
            traceback.print_exc()
    
    def on_value_changed(self):
        """값 변경 이벤트"""
        self.update_count()
        if self.on_data_change:
            self.on_data_change()
    
    def add_row(self, value: str = "", skip_callback: bool = False):
        """새로운 행 추가"""
        item_id = self.tree.insert("", "end", values=(value,))
        self.update_count()
        
        if not skip_callback and self.on_data_change:
            self.on_data_change()
    
    def delete_selected(self):
        """선택된 행 삭제"""
        selected = self.tree.selection()
        if selected:
            for item in selected:
                self.tree.delete(item)
            self.update_count()
            if self.on_data_change:
                self.on_data_change()
        else:
            # 선택된 항목이 없으면 마지막 행 삭제
            children = self.tree.get_children()
            if children:
                self.tree.delete(children[-1])
                self.update_count()
                if self.on_data_change:
                    self.on_data_change()
    
    def on_selection_change(self, event=None):
        """선택 변경 이벤트"""
        # 값 변경 감지를 위해 사용
        pass
    
    def update_count(self):
        """입력 개수 업데이트"""
        count = sum(1 for item in self.tree.get_children() 
                   if self.tree.item(item, 'values')[0].strip())
        self.count_label.configure(text=f"{count}개")
    
    def load_file(self):
        """파일 로드 다이얼로그"""
        if self.is_reference:
            filetypes = [("Excel files", "*.xlsx"), ("All files", "*.*")]
        else:
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        
        file_path = filedialog.askopenfilename(
            title="파일 선택",
            filetypes=filetypes
        )
        
        if file_path:
            self.current_file_path = file_path
            self.load_file_content(file_path)
    
    def load_file_content(self, file_path: str):
        """파일 내용을 그리드에 로드"""
        try:
            if self.is_reference and file_path.endswith('.xlsx'):
                # 엑셀 파일은 파일 경로만 저장
                self.current_file_path = file_path
            else:
                # 텍스트 파일: 한 줄씩 읽어서 그리드에 추가
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]
                
                # 기존 데이터 모두 제거
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # 데이터 추가
                for line in lines:
                    self.add_row(line, skip_callback=True)
                
                # 빈 행이 없으면 하나 추가
                if not lines:
                    self.add_row(skip_callback=True)
            
            self.update_count()
            if self.on_data_change:
                self.on_data_change()
        except Exception as e:
            print(f"파일 로드 오류: {e}")
    
    def clear_data(self):
        """데이터 초기화"""
        # 모든 행 제거
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 빈 행 하나 추가
        self.add_row(skip_callback=True)
        
        self.current_file_path = None
        self.update_count()
        if self.on_data_change:
            self.on_data_change()
    
    def get_text_content(self) -> str:
        """입력된 텍스트 내용 반환 (줄 단위)"""
        lines = []
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values and values[0].strip():
                lines.append(values[0].strip())
        return "\n".join(lines)
    
    def get_file_path(self) -> Optional[str]:
        """현재 로드된 파일 경로 반환"""
        return self.current_file_path
