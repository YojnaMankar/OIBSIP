"""
BMI Logic Module - OASIS INFOBYTE Task 2: BMI Calculator (Advanced)
Handles calculations, category classification, and input validation.
"""

from typing import Tuple, Dict, Any


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate BMI using the standard formula:
        BMI = weight (kg) / (height (m) ^ 2)
    Returns BMI rounded to 2 decimal places.
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def get_bmi_category(bmi: float) -> Tuple[str, str, str]:
    """
    Determine the BMI category, associated visual color, and health advice.
    
    Standard WHO Categories:
        - Underweight: BMI < 18.5
        - Normal:      18.5 <= BMI <= 24.9
        - Overweight:  25.0 <= BMI <= 29.9
        - Obese:       BMI >= 30.0
        
    Returns:
        (category_name, hex_color, advice_string)
    """
    if bmi < 18.5:
        return (
            "Underweight",
            "#0284c7",  # Sky Blue
            "Your BMI indicates you are underweight. Consider consulting a nutritionist for healthy weight gain strategies."
        )
    elif 18.5 <= bmi <= 24.9:
        return (
            "Normal",
            "#16a34a",  # Emerald Green
            "Congratulations! Your BMI is in the healthy/normal weight range. Keep up your balanced lifestyle."
        )
    elif 25.0 <= bmi <= 29.9:
        return (
            "Overweight",
            "#d97706",  # Amber Orange
            "Your BMI indicates you are overweight. Adopting regular physical activity and a balanced diet is recommended."
        )
    else:
        return (
            "Obese",
            "#dc2626",  # Rose Red
            "Your BMI indicates obesity. We recommend consulting a healthcare professional for personalized guidance."
        )


def calculate_healthy_weight_range(height_m: float) -> Tuple[float, float]:
    """
    Calculate the healthy weight range (kg) for a given height in meters
    based on the normal BMI range (18.5 - 24.9).
    """
    if height_m <= 0:
        return (0.0, 0.0)
    min_w = round(18.5 * (height_m ** 2), 1)
    max_w = round(24.9 * (height_m ** 2), 1)
    return (min_w, max_w)


def validate_inputs(user_name: str, weight_str: str, height_str: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validate all inputs before calculation.
    
    Validation Rules:
        - user_name cannot be empty.
        - weight cannot be empty and must be a valid positive float.
        - height cannot be empty and must be a valid positive float.
        - zero or negative values are strictly rejected.
        - practical bounds: weight (10 to 500 kg), height (0.5 to 2.8 meters).
        - helpful error message if user accidentally enters height in centimeters (> 3.0).
        
    Returns:
        (is_valid: bool, error_message: str, parsed_data: dict)
    """
    cleaned_name = user_name.strip()
    if not cleaned_name:
        return (False, "User Name cannot be empty. Please enter a valid name.", {})
    
    if len(cleaned_name) > 50:
        return (False, "User Name is too long. Please use 50 characters or fewer.", {})

    # Validate weight
    weight_raw = weight_str.strip()
    if not weight_raw:
        return (False, "Weight cannot be empty. Please enter your weight in kilograms.", {})
    try:
        weight_kg = float(weight_raw)
    except ValueError:
        return (False, f"Invalid weight value '{weight_raw}'. Weight must be a valid numeric number.", {})
        
    if weight_kg <= 0:
        return (False, "Weight must be a positive number greater than zero.", {})
    if weight_kg < 10.0 or weight_kg > 500.0:
        return (False, f"Weight value '{weight_kg} kg' is outside realistic limits (10 - 500 kg).", {})

    # Validate height
    height_raw = height_str.strip()
    if not height_raw:
        return (False, "Height cannot be empty. Please enter your height in meters (e.g., 1.75).", {})
    try:
        height_m = float(height_raw)
    except ValueError:
        return (False, f"Invalid height value '{height_raw}'. Height must be a valid numeric number.", {})
        
    if height_m <= 0:
        return (False, "Height must be a positive number greater than zero.", {})
        
    # Helpful check if someone entered height in centimeters (e.g., 175 instead of 1.75)
    if height_m > 3.0:
        suggested_m = height_m / 100.0
        return (
            False,
            f"Height '{height_m}' appears to be in centimeters. Please enter height in meters (e.g., {suggested_m:.2f} m).",
            {}
        )
        
    if height_m < 0.5:
        return (False, f"Height '{height_m} m' is too low. Please enter a realistic height in meters (>= 0.5 m).", {})

    return (
        True,
        "",
        {
            "user_name": cleaned_name,
            "weight": round(weight_kg, 2),
            "height": round(height_m, 2),
        }
    )
