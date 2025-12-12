"""
IP Network Matcher & Diff Tool
메인 애플리케이션 진입점
"""
import customtkinter as ctk
from ui.main_window import MainWindow


def main():
    """애플리케이션 메인 함수"""
    # 라이트 테마 설정 (모던한 느낌)
    ctk.set_appearance_mode("light")
    # 기본 테마 사용
    ctk.set_default_color_theme("blue")
    
    # 스케일링 설정 (성능 최적화)
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)
    
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()

