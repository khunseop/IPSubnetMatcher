"""IP 포맷 파싱 모듈"""
from typing import List, Optional, Union
import ipaddress
from utils.ip_utils import parse_ip_input


class IPParser:
    """IP 입력 파싱 클래스"""
    
    @staticmethod
    def parse_text_input(text: str) -> List[dict]:
        """
        텍스트 입력을 파싱하여 IP 리스트 반환
        
        Args:
            text: 입력 텍스트 (줄 단위로 구분)
            
        Returns:
            [{'original': str, 'parsed': IPv4Address|IPv4Network|Set, 'type': str}, ...]
        """
        lines = text.strip().split('\n')
        results = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            parsed = parse_ip_input(line)
            if parsed is None:
                continue
            
            # 타입 결정
            if isinstance(parsed, ipaddress.IPv4Address):
                ip_type = 'Single'
            elif isinstance(parsed, ipaddress.IPv4Network):
                ip_type = 'CIDR'
            elif isinstance(parsed, set):
                ip_type = 'Range'
            else:
                ip_type = 'Unknown'
            
            results.append({
                'original': line,
                'parsed': parsed,
                'type': ip_type
            })
        
        return results
    
    @staticmethod
    def parse_file(file_path: str) -> List[dict]:
        """
        파일에서 IP 리스트 읽기
        
        Args:
            file_path: 파일 경로 (.txt 파일)
            
        Returns:
            파싱된 IP 리스트
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return IPParser.parse_text_input(content)
        except Exception as e:
            print(f"파일 읽기 오류: {e}")
            return []

