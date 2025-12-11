"""IP 매칭 엔진"""
from typing import List, Dict, Optional
import ipaddress
from utils.ip_utils import ip_in_network


class Matcher:
    """IP 매칭 엔진 클래스"""
    
    @staticmethod
    def match(source_list: List[Dict], reference_list: List[Dict]) -> List[Dict]:
        """
        Source IP 리스트와 Reference 네트워크 리스트를 매칭 (여러 매칭 지원)
        
        Args:
            source_list: Source IP 리스트 [{'original': str, 'parsed': ..., 'type': str}, ...]
            reference_list: Reference 네트워크 리스트 [{'original': str, 'parsed': ..., 'type': str}, ...]
            
        Returns:
            매칭 결과 리스트 [{'source': str, 'matched_ips': str}, ...]
            matched_ips는 매칭된 IP들을 콤마로 구분한 문자열
        """
        results = []
        
        for source in source_list:
            source_parsed = source['parsed']
            source_original = source['original']
            
            matched_ips = []
            
            # 모든 Reference와 비교 (여러 매칭 허용)
            for ref in reference_list:
                ref_parsed = ref['parsed']
                ref_original = ref['original']
                
                if ip_in_network(source_parsed, ref_parsed):
                    matched_ips.append(ref_original)
            
            # 매칭된 IP들을 콤마로 구분
            matched_ips_str = ', '.join(matched_ips) if matched_ips else ''
            
            results.append({
                'source': source_original,
                'matched_ips': matched_ips_str
            })
        
        return results

