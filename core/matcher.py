"""IP 매칭 엔진 - 고성능 최적화 버전"""
from typing import List, Dict, Optional, Callable
import ipaddress


class Matcher:
    """IP 매칭 엔진 클래스 - 고성능 최적화"""
    
    @staticmethod
    def match(source_list: List[Dict], reference_list: List[Dict], 
              progress_callback: Optional[Callable[[int, int], None]] = None) -> List[Dict]:
        """
        Source IP 리스트와 Reference 네트워크 리스트를 매칭 (고성능 최적화)
        
        Args:
            source_list: Source IP 리스트
            reference_list: Reference 네트워크 리스트
            progress_callback: 진행률 콜백 함수 (current, total)
            
        Returns:
            매칭 결과 리스트
        """
        return Matcher.match_ultra_optimized(source_list, reference_list, progress_callback)
    
    @staticmethod
    def match_ultra_optimized(source_list: List[Dict], reference_list: List[Dict],
                              progress_callback: Optional[Callable[[int, int], None]] = None) -> List[Dict]:
        """
        초고성능 최적화 매칭
        - Network: prefix 길이별 그룹화 및 정수 변환으로 빠른 비교
        - Address: set으로 O(1) 조회
        - Range: 정수 범위로 변환하여 빠른 비교
        
        Args:
            source_list: Source IP 리스트
            reference_list: Reference 네트워크 리스트
            progress_callback: 진행률 콜백 함수
            
        Returns:
            매칭 결과 리스트
        """
        if not source_list or not reference_list:
            return []
        
        # Reference를 타입별로 그룹화 및 최적화
        network_groups = {}  # prefix 길이별로 그룹화 {prefix_len: [(network_int, original), ...]}
        address_set = {}  # {int(ip): original}
        range_list = []  # [(start_int, end_int, original), ...]
        
        for ref in reference_list:
            ref_parsed = ref['parsed']
            ref_original = ref['original']
            
            if isinstance(ref_parsed, ipaddress.IPv4Network):
                # Network: prefix 길이별로 그룹화
                prefix_len = ref_parsed.prefixlen
                network_int = int(ref_parsed.network_address)
                network_mask = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
                
                if prefix_len not in network_groups:
                    network_groups[prefix_len] = []
                network_groups[prefix_len].append((network_int, network_mask, ref_original))
                
            elif isinstance(ref_parsed, ipaddress.IPv4Address):
                # Address: 정수로 변환하여 dict에 저장 (O(1) 조회)
                addr_int = int(ref_parsed)
                address_set[addr_int] = ref_original
                
            elif isinstance(ref_parsed, tuple):
                # Range: (start_int, end_int) 튜플
                start_int, end_int = ref_parsed
                range_list.append((start_int, end_int, ref_original))
            elif isinstance(ref_parsed, set):
                # Set 타입 (하위 호환성)
                if ref_parsed:
                    sorted_ips = sorted(ref_parsed)
                    start_int = int(sorted_ips[0])
                    end_int = int(sorted_ips[-1])
                    range_list.append((start_int, end_int, ref_original))
        
        results = []
        total_sources = len(source_list)
        
        # Source별로 매칭 수행
        for idx, source in enumerate(source_list):
            source_parsed = source['parsed']
            source_original = source['original']
            
            matched_ips = []
            
            # Source를 정수로 변환
            if isinstance(source_parsed, ipaddress.IPv4Address):
                source_int = int(source_parsed)
                
                # 1. Address 매칭 (O(1))
                if source_int in address_set:
                    matched_ips.append(address_set[source_int])
                
                # 2. Network 매칭 (prefix 길이별로 그룹화하여 빠른 검색)
                for prefix_len in sorted(network_groups.keys(), reverse=True):
                    # 더 긴 prefix부터 확인 (더 구체적인 네트워크 우선)
                    for network_int, network_mask, ref_original in network_groups[prefix_len]:
                        if (source_int & network_mask) == network_int:
                            matched_ips.append(ref_original)
                            # 여러 매칭 허용 (break 제거)
                
                # 3. Range 매칭
                for start_int, end_int, ref_original in range_list:
                    if start_int <= source_int <= end_int:
                        matched_ips.append(ref_original)
                        
            elif isinstance(source_parsed, ipaddress.IPv4Network):
                # Network vs Network/Address/Range 매칭
                source_network_int = int(source_parsed.network_address)
                source_prefix_len = source_parsed.prefixlen
                source_mask = (0xFFFFFFFF << (32 - source_prefix_len)) & 0xFFFFFFFF
                
                # Network 매칭
                for prefix_len in network_groups.keys():
                    for network_int, network_mask, ref_original in network_groups[prefix_len]:
                        # 네트워크 겹침 확인
                        if (source_network_int & network_mask) == network_int or \
                           (network_int & source_mask) == source_network_int:
                            matched_ips.append(ref_original)
                
                # Address 매칭 (Network에 포함되는지)
                for addr_int, ref_original in address_set.items():
                    if (addr_int & source_mask) == source_network_int:
                        matched_ips.append(ref_original)
                
                # Range 매칭
                for start_int, end_int, ref_original in range_list:
                    # Range의 시작/끝이 Network에 포함되는지 확인
                    if (start_int & source_mask) == source_network_int or \
                       (end_int & source_mask) == source_network_int:
                        matched_ips.append(ref_original)
                        
            elif isinstance(source_parsed, tuple):
                # Range vs Network/Address/Range 매칭
                source_start, source_end = source_parsed
                
                # Network 매칭 (Range의 시작/끝이 Network에 포함되는지)
                for prefix_len in network_groups.keys():
                    for network_int, network_mask, ref_original in network_groups[prefix_len]:
                        if ((source_start & network_mask) == network_int) or \
                           ((source_end & network_mask) == network_int):
                            matched_ips.append(ref_original)
                
                # Address 매칭
                for addr_int, ref_original in address_set.items():
                    if source_start <= addr_int <= source_end:
                        matched_ips.append(ref_original)
                
                # Range 매칭 (범위 겹침 확인)
                for start_int, end_int, ref_original in range_list:
                    if not (source_end < start_int or source_start > end_int):
                        matched_ips.append(ref_original)
                        
            elif isinstance(source_parsed, set):
                # Set vs Network/Address/Range 매칭 (하위 호환성)
                source_ips = sorted(source_parsed)
                
                # Network 매칭
                for prefix_len in network_groups.keys():
                    for network_int, network_mask, ref_original in network_groups[prefix_len]:
                        for ip in source_ips:
                            if (int(ip) & network_mask) == network_int:
                                matched_ips.append(ref_original)
                                break
                
                # Address 매칭
                for ip in source_ips:
                    ip_int = int(ip)
                    if ip_int in address_set:
                        matched_ips.append(address_set[ip_int])
                
                # Range 매칭
                for start_int, end_int, ref_original in range_list:
                    for ip in source_ips:
                        ip_int = int(ip)
                        if start_int <= ip_int <= end_int:
                            matched_ips.append(ref_original)
                            break
            
            # 중복 제거 및 정렬
            matched_ips_unique = list(dict.fromkeys(matched_ips))  # 순서 유지하며 중복 제거
            
            # 매칭된 IP들을 콤마로 구분
            matched_ips_str = ', '.join(matched_ips_unique) if matched_ips_unique else ''
            
            results.append({
                'source': source_original,
                'matched_ips': matched_ips_str
            })
            
            # 진행률 콜백 호출 (매 50개마다 또는 마지막)
            if progress_callback and (idx % 50 == 0 or idx == total_sources - 1):
                progress_callback(idx + 1, total_sources)
        
        return results
