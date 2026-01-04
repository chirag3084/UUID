import uuid
import secrets

def generate_chatbot_uuid(company: str, p_type: str, p_num: int, chat_id: int) -> uuid.UUID:
    # 1. Company (3 chars -> 6 hex digits)
    company_hex = company.encode("utf-8").hex()[:6].ljust(6, "0")

    # 2. Project Type (2 chars -> 4 hex digits)
    type_hex = p_type.encode("utf-8").hex()[:4].ljust(4, "0")

    # 3. Project Num (3 hex digits) 
    proj_hex = format(p_num & 0xFFF, "03x")

    # 4. Chat ID (10 hex digits)
    chat_hex = format(chat_id & 0xFFFFFFFFFF, "010x")

    # 5. Fill remaining space with true randomness (9 hex digits)
    # This prevents the trailing "00000" and makes it harder to guess.
    random_padding = secrets.token_hex(5)[:9]

    # Combine into a raw 32-character string
    raw_hex = (company_hex + type_hex + proj_hex + chat_hex + random_padding)[:32]

    # 6. FORCE RFC-4122 Compliance
    valid_list = list(raw_hex)
    valid_list[12] = "4"  # Position 13: Version must be 4
    valid_list[16] = "8"  # Position 17: Variant must be 8, 9, a, or b
    
    final_hex = "".join(valid_list)
    return uuid.UUID(hex=final_hex)

# --- Execute ---
new_uuid = generate_chatbot_uuid("DYZ", "UI", 123, 9876543210)

print(f"New Secure UUID: {new_uuid}")
print(f"Version Check:   {new_uuid.version}")
