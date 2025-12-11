"""IP 포맷 파싱 모듈 - 고성능 배치 처리"""
from typing import List, Optional, Union, Callable, Iterator
import ipaddress
import re
from utils.ip_utils import parse_ip_input


class IPParser:
    """IP 입력 파싱 클래스 - 배치 처리 및 비동기 지원"""
    
    # 배치 크기 (한 번에 처리할 항목 수) - 성능과 UI 반응성의 균형
    BATCH_SIZE = 500  # 적당한 크기로 성능 유지하면서 UI 업데이트 가능
    
    @staticmethod
    def parse_text_input(text: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> List[dict]:
        """
        텍스트 입력을 파싱하여 IP 리스트 반환 (콤마/개행 지원, 배치 처리)
        
        Args:
            text: 입력 텍스트 (개행 또는 콤마로 구분)
            progress_callback: 진행률 콜백 함수 (current, total)
            
        Returns:
            [{'original': str, 'parsed': IPv4Address|IPv4Network|Set, 'type': str}, ...]
        """
        # 빠른 분리 (정규식 최적화)
        items = re.split(r'[,\n\r]+', text.strip())
        # 빈 항목 제거 및 공백 제거 (리스트 컴프리헨션으로 빠르게)
        items = [item.strip() for item in items if item.strip()]
        
        total = len(items)
        if total == 0:
            return []
        
        results = []
        
        # 배치로 처리하여 UI 업데이트 가능
        for batch_start in range(0, total, IPParser.BATCH_SIZE):
            batch_end = min(batch_start + IPParser.BATCH_SIZE, total)
            batch_items = items[batch_start:batch_end]
            
            # 배치 파싱 (벌크 처리)
            batch_results = IPParser._parse_batch(batch_items)
            results.extend(batch_results)
            
            # 진행률 업데이트 (콜백이 있으면 호출)
            if progress_callback:
                progress_callback(batch_end, total)
                # 스레드에서 실행 중이므로 매우 짧은 대기로 GIL이 다른 스레드에 양보
                # 너무 길면 성능 저하, 너무 짧으면 의미 없음
                import time
                time.sleep(0.001)  # 1ms 대기로 UI 스레드에 최소한의 시간 제공
        
        return results
    
    @staticmethod
    def _parse_batch(items: List[str]) -> List[dict]:
        """배치 단위로 빠르게 파싱"""
        results = []
        
        for item in items:
            # 빠른 파싱 (최적화된 버전)
            parsed = IPParser._fast_parse_ip(item)
            if parsed is None:
                continue
            
            # 타입 결정
            if isinstance(parsed, ipaddress.IPv4Address):
                ip_type = 'Single'
            elif isinstance(parsed, ipaddress.IPv4Network):
                ip_type = 'CIDR'
            elif isinstance(parsed, tuple):  # Range는 (start, end) 튜플로 저장
                ip_type = 'Range'
            else:
                ip_type = 'Unknown'
            
            results.append({
                'original': item,
                'parsed': parsed,
                'type': ip_type
            })
        
        return results
    
    @staticmethod
    def _fast_parse_ip(ip_str: str) -> Optional[Union[ipaddress.IPv4Address, ipaddress.IPv4Network, tuple]]:
        """
        빠른 IP 파싱 (Range는 Set 대신 튜플로 저장하여 메모리 절약)
        
        Args:
            ip_str: IP 문자열
            
        Returns:
            IPv4Address, IPv4Network, 또는 (start_int, end_int) 튜플
        """
        ip_str = ip_str.strip()
        if not ip_str:
            return None
        
        # CIDR 포맷 확인 (가장 빠름)
        if '/' in ip_str:
            try:
                return ipaddress.IPv4Network(ip_str, strict=False)
            except ValueError:
                return None
        
        # Range 포맷 확인
        if '-' in ip_str and ip_str.count('-') == 1:
            try:
                parts = ip_str.split('-')
                start_ip = ipaddress.IPv4Address(parts[0].strip())
                end_ip = ipaddress.IPv4Address(parts[1].strip())
                
                if start_ip > end_ip:
                    return None
                
                # Set 대신 튜플로 저장 (메모리 절약, 빠른 비교)
                return (int(start_ip), int(end_ip))
            except (ValueError, AttributeError):
                return None
        
        # Single IP
        try:
            return ipaddress.IPv4Address(ip_str)
        except ValueError:
            return None
    
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
