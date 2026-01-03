import uuid
import secrets

def generate_chatbot_uuid(
    company: str, p_type: str, p_num: int, chat_id: int
) -> uuid.UUID:
    # 1. Company (3 chars -> 6 hex digits)
    # Encodes string to hex, takes first 6 chars, pads with '0' if string is too short
    company_hex = company.encode("utf-8").hex()[:6].ljust(6, "0")

    # 2. Project Type (3 chars -> 6 hex digits)
    type_hex = p_type.encode("utf-8").hex()[:6].ljust(6, "0")

    # 3. Project Num (6 hex digits) - Reduced to fit new sizes
    # Supports up to 16,777,215 (0xFFFFFF)
    proj_hex = format(p_num & 0xFFFFFF, "06x")

    # 4. Chat ID (10 hex digits)
    # Supports up to 1,099,511,627,775
    chat_hex = format(chat_id & 0xFFFFFFFFFF, "010x")

    # 5. Random (4 hex digits)
    rand_hex = secrets.token_hex(2)

    # Combine (6 + 6 + 6 + 10 + 4 = 32 hex chars)
    combined_hex = company_hex + type_hex + proj_hex + chat_hex + rand_hex

    return uuid.UUID(hex=combined_hex)

def parse_chatbot_uuid(u: uuid.UUID) -> dict:
    h = u.hex
    return {
        "company_code": bytes.fromhex(h[0:6]).decode("utf-8", errors="ignore").strip('\x00'),
        "type_code": bytes.fromhex(h[6:12]).decode("utf-8", errors="ignore").strip('\x00'),
        "project_num": h[12:18],
        "chat_id": h[18:28],
        "random_salt": h[28:32],
    }

# --- Execute ---
# Example with 3-character codes
my_uuid = generate_chatbot_uuid("DYZ", "UIUX", 123456, 9876543210)

print(f"Valid UUID: {my_uuid}")
print(f"Parsed:     {parse_chatbot_uuid(my_uuid)}")
