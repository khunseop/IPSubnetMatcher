"""
IP Network Matcher & Diff Tool
메인 애플리케이션 진입점
"""
import customtkinter as ctk
from ui.main_window import MainWindow


def main():
    """애플리케이션 메인 함수"""
    # 모던 다크 테마 설정
    ctk.set_appearance_mode("dark")
    # 커스텀 색상 테마 설정 (모던한 블루-퍼플 그라데이션)
    ctk.set_default_color_theme("blue")
    
    # 커스텀 색상 팔레트 적용
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)
    
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()

