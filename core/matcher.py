"""IP 매칭 엔진 - 최적화 버전"""
from typing import List, Dict, Optional
import ipaddress
from utils.ip_utils import ip_in_network


class Matcher:
    """IP 매칭 엔진 클래스 - 성능 최적화"""
    
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
        return Matcher.match_optimized(source_list, reference_list)
    
    @staticmethod
    def match_optimized(source_list: List[Dict], reference_list: List[Dict]) -> List[Dict]:
        """
        최적화된 매칭 (Reference를 타입별로 그룹화하여 빠른 검색)
        
        Args:
            source_list: Source IP 리스트
            reference_list: Reference 네트워크 리스트
            
        Returns:
            매칭 결과 리스트
        """
        if not source_list or not reference_list:
            return []
        
        # Reference를 타입별로 그룹화 (성능 향상)
        networks = []  # IPv4Network 리스트
        addresses = []  # IPv4Address 리스트
        ranges = []  # Set 리스트
        
        for ref in reference_list:
            ref_parsed = ref['parsed']
            if isinstance(ref_parsed, ipaddress.IPv4Network):
                networks.append(ref)
            elif isinstance(ref_parsed, ipaddress.IPv4Address):
                addresses.append(ref)
            elif isinstance(ref_parsed, set):
                ranges.append(ref)
        
        results = []
        
        # Source별로 매칭 수행
        for source in source_list:
            source_parsed = source['parsed']
            source_original = source['original']
            
            matched_ips = []
            
            # Network 타입 매칭 (가장 빠름)
            if networks:
                for ref in networks:
                    if ip_in_network(source_parsed, ref['parsed']):
                        matched_ips.append(ref['original'])
            
            # Address 타입 매칭
            if addresses:
                for ref in addresses:
                    if ip_in_network(source_parsed, ref['parsed']):
                        matched_ips.append(ref['original'])
            
            # Range 타입 매칭 (가장 느림, 마지막에)
            if ranges:
                for ref in ranges:
                    if ip_in_network(source_parsed, ref['parsed']):
                        matched_ips.append(ref['original'])
            
            # 매칭된 IP들을 콤마로 구분
            matched_ips_str = ', '.join(matched_ips) if matched_ips else ''
            
            results.append({
                'source': source_original,
                'matched_ips': matched_ips_str
            })
        
        return results
