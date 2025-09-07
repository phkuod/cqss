"""
DEPRECATED: This file is deprecated and will be removed in v3.0.0
Use data_processor_v2.py and models.py instead for the clean unified API.

Kept for backward compatibility during migration.
"""

import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Any
import warnings

warnings.warn(
    "data_processor.py is deprecated. Use 'from src.data_processor_v2 import load_projects' instead.",
    DeprecationWarning,
    stacklevel=2
)

class ProjectDataProcessor:
    """
    Processes CSV project data and converts it to format suitable for D3.js Gantt chart
    """
    
    def __init__(self):
        # Legacy format columns
        self.legacy_required_columns = [
            'project_name', 'category', 'priority', 'preparing_start', 
            'preparing_end', 'execution_end', 'progress_percent', 
            'description', 'team_lead'
        ]
        
        # Multi-stage format columns
        self.multistage_required_columns = [
            'project_name', 'category', 'priority', 'description', 
            'team_lead', 'stages'
        ]
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Load and validate CSV file"""
        try:
            df = pd.read_csv(file_path)
            self._validate_columns(df)
            self._validate_data_types(df)
            return df
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {str(e)}")
    
    def _validate_columns(self, df: pd.DataFrame) -> None:
        """Validate that all required columns are present"""
        # Check if it's legacy format or multi-stage format
        if 'stages' in df.columns:
            # Multi-stage format
            missing_columns = set(self.multistage_required_columns) - set(df.columns)
            if missing_columns:
                raise ValueError(f"Missing required columns for multi-stage format: {missing_columns}")
        else:
            # Legacy format
            missing_columns = set(self.legacy_required_columns) - set(df.columns)
            if missing_columns:
                raise ValueError(f"Missing required columns for legacy format: {missing_columns}")
    
    def _validate_data_types(self, df: pd.DataFrame) -> None:
        """Validate and convert data types"""
        if 'stages' in df.columns:
            # Multi-stage format validation
            self._validate_multistage_data(df)
        else:
            # Legacy format validation
            self._validate_legacy_data(df)
    
    def _validate_legacy_data(self, df: pd.DataFrame) -> None:
        """Validate legacy format data"""
        # Convert date columns
        date_columns = ['preparing_start', 'preparing_end', 'execution_end']
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception as e:
                raise ValueError(f"Invalid date format in column '{col}': {str(e)}")
        
        # Validate progress percentage
        if not df['progress_percent'].between(0, 100).all():
            raise ValueError("Progress percentage must be between 0 and 100")
        
        # Validate status columns if present
        valid_statuses = ['normal', 'critical', 'warning', 'completed', 'delayed']
        for status_col in ['preparing_status', 'execution_status']:
            if status_col in df.columns:
                invalid_statuses = df[~df[status_col].isin(valid_statuses)][status_col].unique()
                if len(invalid_statuses) > 0:
                    raise ValueError(f"Invalid status values in column '{status_col}': {invalid_statuses}. Must be one of {valid_statuses}")
        
        # Validate date logic
        for idx, row in df.iterrows():
            if row['preparing_start'] >= row['preparing_end']:
                raise ValueError(f"Row {idx}: Preparing start date must be before end date")
            if row['preparing_end'] >= row['execution_end']:
                raise ValueError(f"Row {idx}: Preparing end date must be before execution end date")
    
    def _validate_multistage_data(self, df: pd.DataFrame) -> None:
        """Validate multi-stage format data"""
        for idx, row in df.iterrows():
            try:
                stages = json.loads(row['stages'])
                if not isinstance(stages, list) or len(stages) < 1:
                    raise ValueError(f"Row {idx}: Stages must be a non-empty list")
                
                prev_end = None
                for stage_idx, stage in enumerate(stages):
                    # Validate required stage fields
                    required_fields = ['name', 'start', 'end', 'progress']
                    for field in required_fields:
                        if field not in stage:
                            raise ValueError(f"Row {idx}, Stage {stage_idx}: Missing required field '{field}'")
                    
                    # Validate dates
                    try:
                        start_date = pd.to_datetime(stage['start'])
                        end_date = pd.to_datetime(stage['end'])
                    except Exception as e:
                        raise ValueError(f"Row {idx}, Stage {stage_idx}: Invalid date format - {str(e)}")
                    
                    # Validate date logic
                    if start_date >= end_date:
                        raise ValueError(f"Row {idx}, Stage {stage_idx}: Start date must be before end date")
                    
                    # Validate sequential stages (optional - stages can overlap)
                    if prev_end and start_date < prev_end:
                        # Warning: stages overlap, but allow it
                        pass
                    
                    # Validate progress
                    progress = stage['progress']
                    if not isinstance(progress, (int, float)) or not 0 <= progress <= 100:
                        raise ValueError(f"Row {idx}, Stage {stage_idx}: Progress must be between 0 and 100")
                    
                    # Validate status field if present
                    if 'status' in stage:
                        valid_statuses = ['normal', 'critical', 'warning', 'completed', 'delayed']
                        if stage['status'] not in valid_statuses:
                            raise ValueError(f"Row {idx}, Stage {stage_idx}: Status must be one of {valid_statuses}")
                    
                    prev_end = end_date
                    
            except json.JSONDecodeError as e:
                raise ValueError(f"Row {idx}: Invalid JSON format in stages column - {str(e)}")
            except Exception as e:
                if "Row" not in str(e):
                    raise ValueError(f"Row {idx}: {str(e)}")
                else:
                    raise
    
    def process_to_gantt_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Convert DataFrame to format suitable for D3.js Gantt chart"""
        gantt_data = []
        
        for idx, row in df.iterrows():
            if 'stages' in df.columns:
                # Multi-stage format
                project_data = self._process_multistage_project(idx, row)
            else:
                # Legacy format
                project_data = self._process_legacy_project(idx, row)
            
            gantt_data.append(project_data)
        
        return gantt_data
    
    def _process_legacy_project(self, idx: int, row: pd.Series) -> Dict[str, Any]:
        """Process legacy format project data"""
        # Convert legacy format to new multi-stage structure
        stages = [
            {
                'name': 'Preparing',
                'start': row['preparing_start'].isoformat(),
                'end': row['preparing_end'].isoformat(),
                'duration_days': (row['preparing_end'] - row['preparing_start']).days,
                'progress_percent': 100,  # Preparing stage is always complete if execution has started
                'status': row.get('preparing_status', 'normal')  # Add status support
            },
            {
                'name': 'Execution',
                'start': row['preparing_end'].isoformat(),
                'end': row['execution_end'].isoformat(),
                'duration_days': (row['execution_end'] - row['preparing_end']).days,
                'progress_percent': int(row['progress_percent']),
                'status': row.get('execution_status', 'normal')  # Add status support
            }
        ]
        
        project_data = {
            'id': f"project_{idx}",
            'name': row['project_name'],
            'category': row['category'],
            'priority': row['priority'],
            'description': row['description'],
            'team_lead': row['team_lead'],
            'stages': stages,
            'total_duration_days': (row['execution_end'] - row['preparing_start']).days
        }
        
        return project_data
    
    def _process_multistage_project(self, idx: int, row: pd.Series) -> Dict[str, Any]:
        """Process multi-stage format project data"""
        stages_json = json.loads(row['stages'])
        
        # Process each stage
        stages = []
        all_start_dates = []
        all_end_dates = []
        
        for stage_data in stages_json:
            start_date = pd.to_datetime(stage_data['start'])
            end_date = pd.to_datetime(stage_data['end'])
            
            stage = {
                'name': stage_data['name'],
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'duration_days': (end_date - start_date).days,
                'progress_percent': int(stage_data['progress']),
                'status': stage_data.get('status', 'normal')  # Add status support with default
            }
            stages.append(stage)
            all_start_dates.append(start_date)
            all_end_dates.append(end_date)
        
        # Calculate total duration
        total_start = min(all_start_dates)
        total_end = max(all_end_dates)
        
        project_data = {
            'id': f"project_{idx}",
            'name': row['project_name'],
            'category': row['category'],
            'priority': row['priority'],
            'description': row['description'],
            'team_lead': row['team_lead'],
            'stages': stages,
            'total_duration_days': (total_end - total_start).days
        }
        
        return project_data
    
    def export_to_json(self, data: List[Dict[str, Any]], output_path: str) -> None:
        """Export processed data to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_date_range(self, data: List[Dict[str, Any]]) -> Dict[str, str]:
        """Get overall date range for the chart"""
        all_start_dates = []
        all_end_dates = []
        
        for proj in data:
            # Use stages for accurate date range
            for stage in proj['stages']:
                all_start_dates.append(datetime.fromisoformat(stage['start']))
                all_end_dates.append(datetime.fromisoformat(stage['end']))
        
        return {
            'min_date': min(all_start_dates).isoformat(),
            'max_date': max(all_end_dates).isoformat()
        }

# Example usage
if __name__ == "__main__":
    processor = ProjectDataProcessor()
    
    # Load and process sample data
    df = processor.load_csv('../data/sample_projects.csv')
    gantt_data = processor.process_to_gantt_data(df)
    
    # Export to JSON
    processor.export_to_json(gantt_data, '../output/projects_data.json')
    
    # Get date range
    date_range = processor.get_date_range(gantt_data)
    print(f"Date range: {date_range['min_date']} to {date_range['max_date']}")
    print(f"Processed {len(gantt_data)} projects successfully")