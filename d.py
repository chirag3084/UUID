import secrets
import string
import re


def generate_custom_uuid(
    company_code, project_type, project_num, chat_id, random_bits=32
):
    """
    Generates a structured ID:
    COMPANY(4)-TYPE(4)-PROJ(6 hex)-CHAT(8 hex)-RAND(8 hex)
    """
    # 1. Clean Company Code (Pad to 4 chars)
    comp = company_code.upper()[:4].zfill(4)

    # 2. Clean Project Type (Limit to 4 chars for symmetry)
    p_type = project_type.upper()[:4].zfill(4)

    # 3. Convert Project Num to 6-char Hexadecimal
    # :06x converts to hex and pads to 6 digits
    pnum_hex = f"{int(project_num):06x}".upper()

    # 4. Convert Chat ID to 8-char Hexadecimal
    chat_hex = f"{int(chat_id):08x}".upper()

    # 5. Generate Random Hex (32 bits = 8 hex chars)
    rand_hex = secrets.token_hex(random_bits // 8).upper()

    return f"{comp}-{p_type}-{pnum_hex}-{chat_hex}-{rand_hex}"


def validate_custom_uuid(uuid_str):
    # Updated pattern to allow Hex (0-9 and A-F)
    pattern = r"^[A-Z0-9]{4}-[A-Z0-9]{4}-[0-9A-F]{6}-[0-9A-F]{8}-[0-9A-F]{8}$"
    return bool(re.match(pattern, uuid_str))


# --- Test ---
# Project 123456 -> 01E240
# Chat 78901234  -> 04B0F3F2
my_uuid = generate_custom_uuid("WDYZ", "SEHO", 4555674, 78901234)


print(f"Generated UUID: {my_uuid}")
print(f"Is Valid:      {validate_custom_uuid(my_uuid)}")
