from typing import Dict, List, Any
import re

def evaluate_condition(stock_data: Dict[str, Any], condition: str) -> bool:
    """
    Evaluate a single condition against stock data.
    Supports comparison operators: >, <, >=, <=, ==, !=
    Handles Excel-specific numeric formats and missing values
    """
    try:
        # Handle empty/null values
        if pd.isna(stock_data.get(condition.strip(), None)):
            return False
            
        # Extract field and comparison
        match = re.match(r"(.+?)\s*(>|<|>=|<=|==|!=)\s*(.+)", condition.strip())
        if not match:
            # Simple boolean check if no operator
            value = stock_data.get(condition.strip())
            if isinstance(value, (bool, str)):
                return str(value).lower() == "true"
            return bool(value)
        
        field, op, value = match.groups()
        field = field.strip()
        value = value.strip()
        
        # Get the field value from stock data
        field_value = stock_data.get(field)
        if field_value is None:
            return False
            
        # Handle numeric comparisons (including Excel numeric formats)
        if isinstance(field_value, (int, float, str)):
            try:
                # Convert both to float for comparison
                field_num = float(field_value)
                num_value = float(value)
                if op == ">": return field_num > num_value
                if op == "<": return field_num < num_value
                if op == ">=": return field_num >= num_value
                if op == "<=": return field_num <= num_value
                if op == "==": return field_num == num_value
                if op == "!=": return field_num != num_value
            except (ValueError, TypeError):
                # Fall back to string comparison if numeric fails
                if op == "==": return str(field_value).lower() == value.lower()
                if op == "!=": return str(field_value).lower() != value.lower()
                return False
        # Handle string comparisons
        elif isinstance(field_value, str):
            if op == "==": return field_value.lower() == value.lower()
            if op == "!=": return field_value.lower() != value.lower()
            
        return False
    except Exception as e:
        print(f"Error evaluating condition '{condition}': {str(e)}")
        return False

def filter_stocks(stocks_data: Dict[str, Dict[str, Any]], conditions: List[str], limit: int = 20) -> List[Dict[str, Any]]:
    """
    Filter stocks based on multiple conditions.
    Returns list of matching stocks with symbol and data.
    """
    results = []
    for symbol, data in stocks_data.items():
        matches_all = True
        for condition in conditions:
            if not evaluate_condition(data, condition):
                matches_all = False
                break
        if matches_all:
            results.append({"symbol": symbol, "data": data})
            if len(results) >= limit:
                break
    return results