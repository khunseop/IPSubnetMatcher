"""IP 매칭 엔진"""
from typing import List, Dict, Optional
import ipaddress
from utils.ip_utils import ip_in_network


class Matcher:
    """IP 매칭 엔진 클래스"""
    
    @staticmethod
    def match(source_list: List[Dict], reference_list: List[Dict]) -> List[Dict]:
        """
        Source IP 리스트와 Reference 네트워크 리스트를 매칭
        
        Args:
            source_list: Source IP 리스트 [{'original': str, 'parsed': ..., 'type': str}, ...]
            reference_list: Reference 네트워크 리스트 [{'network_name': str, 'parsed': ..., 'location': str, ...}, ...]
            
        Returns:
            매칭 결과 리스트 [{'source': str, 'type': str, 'matched': bool, 
                              'matched_network_name': str, 'matched_location': str, 
                              'matched_cidr': str}, ...]
        """
        results = []
        
        for source in source_list:
            source_parsed = source['parsed']
            source_original = source['original']
            source_type = source['type']
            
            matched = False
            matched_network_name = ''
            matched_location = ''
            matched_cidr = ''
            
            # 모든 Reference와 비교
            for ref in reference_list:
                ref_parsed = ref['parsed']
                
                if ip_in_network(source_parsed, ref_parsed):
                    matched = True
                    matched_network_name = ref['network_name']
                    matched_location = ref['location']
                    
                    # CIDR 표시 형식 결정
                    if isinstance(ref_parsed, ipaddress.IPv4Network):
                        matched_cidr = str(ref_parsed)
                    elif isinstance(ref_parsed, ipaddress.IPv4Address):
                        matched_cidr = str(ref_parsed)
                    elif isinstance(ref_parsed, set):
                        # Range의 경우 첫 번째와 마지막 IP 표시
                        sorted_ips = sorted(ref_parsed)
                        if len(sorted_ips) > 0:
                            matched_cidr = f"{sorted_ips[0]}-{sorted_ips[-1]}"
                    
                    # 하나만 매칭되면 중단 (여러 개 매칭 시 첫 번째 선택)
                    break
            
            results.append({
                'source': source_original,
                'type': source_type,
                'matched': matched,
                'matched_network_name': matched_network_name,
                'matched_location': matched_location,
                'matched_cidr': matched_cidr
            })
        
        return results

