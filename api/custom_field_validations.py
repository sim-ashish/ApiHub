import re

def email_validation(value: str) -> bool:
    email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    # Use re.match to check if the email matches the pattern
    if re.match(email_pattern, value):
        return True
    else:
        return False
    

def mobile_validation(country: str, value: str) -> bool:
    pass