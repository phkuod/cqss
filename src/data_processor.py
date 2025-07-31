import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Any

class ProjectDataProcessor:
    """
    Processes CSV project data and converts it to format suitable for D3.js Gantt chart
    """
    
    def __init__(self):
        self.required_columns = [
            'project_name', 'category', 'priority', 'preparing_start', 
            'preparing_end', 'execution_end', 'progress_percent', 
            'description', 'team_lead'
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
        missing_columns = set(self.required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    def _validate_data_types(self, df: pd.DataFrame) -> None:
        """Validate and convert data types"""
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
        
        # Validate date logic
        for idx, row in df.iterrows():
            if row['preparing_start'] >= row['preparing_end']:
                raise ValueError(f"Row {idx}: Preparing start date must be before end date")
            if row['preparing_end'] >= row['execution_end']:
                raise ValueError(f"Row {idx}: Preparing end date must be before execution end date")
    
    def process_to_gantt_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Convert DataFrame to format suitable for D3.js Gantt chart"""
        gantt_data = []
        
        for idx, row in df.iterrows():
            project_data = {
                'id': f"project_{idx}",
                'name': row['project_name'],
                'category': row['category'],
                'priority': row['priority'],
                'description': row['description'],
                'team_lead': row['team_lead'],
                'preparing_stage': {
                    'start': row['preparing_start'].isoformat(),
                    'end': row['preparing_end'].isoformat(),
                    'duration_days': (row['preparing_end'] - row['preparing_start']).days
                },
                'execution_stage': {
                    'start': row['preparing_end'].isoformat(),
                    'end': row['execution_end'].isoformat(),
                    'duration_days': (row['execution_end'] - row['preparing_end']).days,
                    'progress_percent': int(row['progress_percent'])
                },
                'total_duration_days': (row['execution_end'] - row['preparing_start']).days
            }
            gantt_data.append(project_data)
        
        return gantt_data
    
    def export_to_json(self, data: List[Dict[str, Any]], output_path: str) -> None:
        """Export processed data to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_date_range(self, data: List[Dict[str, Any]]) -> Dict[str, str]:
        """Get overall date range for the chart"""
        all_start_dates = [datetime.fromisoformat(proj['preparing_stage']['start']) for proj in data]
        all_end_dates = [datetime.fromisoformat(proj['execution_stage']['end']) for proj in data]
        
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