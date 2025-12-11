"""IP 관련 유틸리티 함수 - 최적화 버전"""
import ipaddress
from typing import Union, Set, Optional, Tuple


def parse_ip_range(ip_range: str) -> Optional[Tuple[int, int]]:
    """
    IP Range 포맷을 파싱하여 (시작, 끝) 정수 튜플로 변환 (메모리 효율적)
    예: '192.168.1.1-192.168.1.50' -> (3232235777, 3232235826)
    
    Args:
        ip_range: 하이픈으로 구분된 IP 범위 문자열
        
    Returns:
        (start_int, end_int) 튜플 또는 None (파싱 실패 시)
    """
    try:
        parts = ip_range.strip().split('-')
        if len(parts) != 2:
            return None
        
        start_ip = ipaddress.IPv4Address(parts[0].strip())
        end_ip = ipaddress.IPv4Address(parts[1].strip())
        
        if start_ip > end_ip:
            return None
        
        # Set 대신 정수 범위로 반환 (메모리 절약)
        return (int(start_ip), int(end_ip))
    except (ValueError, AttributeError):
        return None


def parse_ip_input(ip_str: str) -> Optional[Union[ipaddress.IPv4Address, ipaddress.IPv4Network, Tuple[int, int]]]:
    """
    IP 입력 문자열을 파싱하여 적절한 타입으로 변환 (최적화)
    Single IP, CIDR, Range를 자동 감지
    
    Args:
        ip_str: IP 문자열 (Single/CIDR/Range)
        
    Returns:
        IPv4Address, IPv4Network, 또는 (start_int, end_int) 튜플
    """
    ip_str = ip_str.strip()
    if not ip_str:
        return None
    
    # CIDR 포맷 확인
    if '/' in ip_str:
        try:
            return ipaddress.IPv4Network(ip_str, strict=False)
        except ValueError:
            return None
    
    # Range 포맷 확인
    if '-' in ip_str and ip_str.count('-') == 1:
        return parse_ip_range(ip_str)
    
    # Single IP
    try:
        return ipaddress.IPv4Address(ip_str)
    except ValueError:
        return None


def ip_in_network(ip: Union[ipaddress.IPv4Address, ipaddress.IPv4Network, Tuple[int, int], Set], 
                  network: Union[ipaddress.IPv4Address, ipaddress.IPv4Network, Tuple[int, int], Set]) -> bool:
    """
    IP가 네트워크에 포함되는지 확인 (최적화)
    
    Args:
        ip: Source IP (IPv4Address, IPv4Network, (start, end) 튜플, 또는 Set)
        network: Reference 네트워크 (IPv4Address, IPv4Network, (start, end) 튜플, 또는 Set)
        
    Returns:
        포함 여부 (bool)
    """
    # Single IP vs Network
    if isinstance(ip, ipaddress.IPv4Address) and isinstance(network, ipaddress.IPv4Network):
        return ip in network
    
    # Single IP vs Single IP
    if isinstance(ip, ipaddress.IPv4Address) and isinstance(network, ipaddress.IPv4Address):
        return ip == network
    
    # Single IP vs Range (튜플)
    if isinstance(ip, ipaddress.IPv4Address) and isinstance(network, tuple):
        ip_int = int(ip)
        return network[0] <= ip_int <= network[1]
    
    # Network vs Network (겹침 확인)
    if isinstance(ip, ipaddress.IPv4Network) and isinstance(network, ipaddress.IPv4Network):
        return ip.overlaps(network) or ip.subnet_of(network) or network.subnet_of(ip)
    
    # Network vs Range
    if isinstance(ip, ipaddress.IPv4Network) and isinstance(network, tuple):
        # Range의 시작/끝이 Network에 포함되는지 확인
        start_addr = ipaddress.IPv4Address(network[0])
        end_addr = ipaddress.IPv4Address(network[1])
        return start_addr in ip or end_addr in ip
    
    # Range vs Network
    if isinstance(ip, tuple) and isinstance(network, ipaddress.IPv4Network):
        start_addr = ipaddress.IPv4Address(ip[0])
        end_addr = ipaddress.IPv4Address(ip[1])
        return start_addr in network or end_addr in network
    
    # Range vs Range
    if isinstance(ip, tuple) and isinstance(network, tuple):
        # 범위 겹침 확인
        return not (ip[1] < network[0] or ip[0] > network[1])
    
    # Set vs Network (하위 호환성)
    if isinstance(ip, set) and isinstance(network, ipaddress.IPv4Network):
        return any(addr in network for addr in ip)
    
    # Set vs Set
    if isinstance(ip, set) and isinstance(network, set):
        return bool(ip & network)
    
    # Network vs Set
    if isinstance(ip, ipaddress.IPv4Network) and isinstance(network, set):
        return any(addr in ip for addr in network)
    
    return False
