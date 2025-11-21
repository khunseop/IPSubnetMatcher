"""엑셀 파일 처리 모듈"""
import pandas as pd
from typing import List, Dict, Optional
import ipaddress
from utils.ip_utils import parse_ip_input


class ExcelHandler:
    """엑셀 파일 처리 클래스"""
    
    EXPECTED_COLUMNS = ["네트워크ID", "객체명", "네트워크명", "구분", "레벨", "추가속성", "위치"]
    
    @staticmethod
    def load_reference_excel(file_path: str) -> List[Dict]:
        """
        Reference 엑셀 파일 로드 및 파싱
        
        Args:
            file_path: 엑셀 파일 경로
            
        Returns:
            [{'network_id': str, 'object_name': str, 'network_name': str, 
              'category': str, 'level': str, 'attributes': str, 'location': str,
              'parsed': IPv4Address|IPv4Network|Set, 'type': str}, ...]
        """
        try:
            # 3열(C열)부터 시작하므로 usecols로 C열부터 읽기
            # 먼저 전체 파일을 읽어서 헤더 행과 컬럼 위치 확인
            df_full = pd.read_excel(file_path, header=None)
            
            # 첫 번째 행에서 컬럼명 찾기
            header_row = None
            for idx, row in df_full.iterrows():
                row_values = [str(val).strip() if pd.notna(val) else '' for val in row.values]
                # 예상 컬럼명들이 포함되어 있는지 확인 (3열부터 확인)
                # A, B 열을 제외하고 C열(인덱스 2)부터 확인
                if len(row_values) > 2:
                    row_values_from_col3 = row_values[2:]
                    # 예상 컬럼명들이 포함되어 있는지 확인
                    found_cols = sum(1 for col in ExcelHandler.EXPECTED_COLUMNS if col in row_values_from_col3)
                    if found_cols >= len(ExcelHandler.EXPECTED_COLUMNS) * 0.7:  # 70% 이상 일치하면 헤더로 간주
                        header_row = idx
                        break
            
            if header_row is None:
                # 헤더를 찾지 못한 경우, 첫 번째 행을 헤더로 사용
                header_row = 0
            
            # C열(인덱스 2)부터 읽기
            # 전체를 읽은 후 C열부터만 선택하는 방식 사용
            df_full = pd.read_excel(file_path, header=header_row)
            
            # C열(인덱스 2)부터만 선택
            if len(df_full.columns) > 2:
                df = df_full.iloc[:, 2:].copy()
            else:
                df = df_full.copy()
            
            # 컬럼명 정규화 (공백 제거)
            df.columns = df.columns.str.strip()
            
            # 필요한 컬럼 확인 및 매핑
            column_mapping = {}
            for expected_col in ExcelHandler.EXPECTED_COLUMNS:
                for actual_col in df.columns:
                    if expected_col == actual_col or expected_col in str(actual_col):
                        column_mapping[expected_col] = actual_col
                        break
            
            # 필수 컬럼 확인
            required_cols = ["네트워크명", "레벨"]
            if not all(col in column_mapping for col in required_cols):
                raise ValueError(f"필수 컬럼을 찾을 수 없습니다: {required_cols}")
            
            results = []
            
            # 레벨이 '4'인 행만 필터링
            level_col = column_mapping["레벨"]
            network_name_col = column_mapping["네트워크명"]
            
            filtered_df = df[df[level_col].astype(str).str.strip() == '4'].copy()
            
            for _, row in filtered_df.iterrows():
                network_name = str(row[network_name_col]).strip() if pd.notna(row[network_name_col]) else ''
                
                if not network_name:
                    continue
                
                # IP 정보 파싱
                parsed = parse_ip_input(network_name)
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
                
                # 메타데이터 추출
                network_id = str(row[column_mapping.get("네트워크ID", "")]).strip() if "네트워크ID" in column_mapping and pd.notna(row.get(column_mapping["네트워크ID"])) else ''
                object_name = str(row[column_mapping.get("객체명", "")]).strip() if "객체명" in column_mapping and pd.notna(row.get(column_mapping["객체명"])) else ''
                category = str(row[column_mapping.get("구분", "")]).strip() if "구분" in column_mapping and pd.notna(row.get(column_mapping["구분"])) else ''
                attributes = str(row[column_mapping.get("추가속성", "")]).strip() if "추가속성" in column_mapping and pd.notna(row.get(column_mapping["추가속성"])) else ''
                location = str(row[column_mapping.get("위치", "")]).strip() if "위치" in column_mapping and pd.notna(row.get(column_mapping["위치"])) else ''
                
                results.append({
                    'network_id': network_id,
                    'object_name': object_name,
                    'network_name': network_name,
                    'category': category,
                    'level': '4',
                    'attributes': attributes,
                    'location': location,
                    'parsed': parsed,
                    'type': ip_type
                })
            
            return results
            
        except Exception as e:
            print(f"엑셀 파일 처리 오류: {e}")
            raise

