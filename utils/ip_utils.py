"""IP 관련 유틸리티 함수"""
import ipaddress
from typing import Union, Set, Optional


def parse_ip_range(ip_range: str) -> Optional[Set[ipaddress.IPv4Address]]:
    """
    IP Range 포맷을 파싱하여 IP Set으로 변환
    예: '192.168.1.1-192.168.1.50'
    
    Args:
        ip_range: 하이픈으로 구분된 IP 범위 문자열
        
    Returns:
        IP 주소들의 Set 또는 None (파싱 실패 시)
    """
    try:
        parts = ip_range.strip().split('-')
        if len(parts) != 2:
            return None
        
        start_ip = ipaddress.IPv4Address(parts[0].strip())
        end_ip = ipaddress.IPv4Address(parts[1].strip())
        
        if start_ip > end_ip:
            return None
        
        ip_set = set()
        current = int(start_ip)
        end = int(end_ip)
        
        while current <= end:
            ip_set.add(ipaddress.IPv4Address(current))
            current += 1
        
        return ip_set
    except (ValueError, AttributeError):
        return None


def parse_ip_input(ip_str: str) -> Optional[Union[ipaddress.IPv4Address, ipaddress.IPv4Network, Set[ipaddress.IPv4Address]]]:
    """
    IP 입력 문자열을 파싱하여 적절한 타입으로 변환
    Single IP, CIDR, Range를 자동 감지
    
    Args:
        ip_str: IP 문자열 (Single/CIDR/Range)
        
    Returns:
        IPv4Address, IPv4Network, 또는 Set[IPv4Address] 또는 None
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


def ip_in_network(ip: Union[ipaddress.IPv4Address, ipaddress.IPv4Network, Set[ipaddress.IPv4Address]], 
                  network: Union[ipaddress.IPv4Address, ipaddress.IPv4Network, Set[ipaddress.IPv4Address]]) -> bool:
    """
    IP가 네트워크에 포함되는지 확인
    
    Args:
        ip: Source IP (IPv4Address, IPv4Network, 또는 Set)
        network: Reference 네트워크 (IPv4Address, IPv4Network, 또는 Set)
        
    Returns:
        포함 여부 (bool)
    """
    # Single IP vs Network
    if isinstance(ip, ipaddress.IPv4Address) and isinstance(network, ipaddress.IPv4Network):
        return ip in network
    
    # Single IP vs Single IP
    if isinstance(ip, ipaddress.IPv4Address) and isinstance(network, ipaddress.IPv4Address):
        return ip == network
    
    # Network vs Network (겹침 확인)
    if isinstance(ip, ipaddress.IPv4Network) and isinstance(network, ipaddress.IPv4Network):
        return ip.overlaps(network) or ip.subnet_of(network) or network.subnet_of(ip)
    
    # Set vs Network
    if isinstance(ip, set) and isinstance(network, ipaddress.IPv4Network):
        return any(addr in network for addr in ip)
    
    # Set vs Set
    if isinstance(ip, set) and isinstance(network, set):
        return bool(ip & network)
    
    # Network vs Set
    if isinstance(ip, ipaddress.IPv4Network) and isinstance(network, set):
        return any(addr in ip for addr in network)
    
    return False

