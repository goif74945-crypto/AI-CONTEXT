# CHAT_IDS

Registry for unique worker identities using format C-XXXXXXXX, where XXXXXXXX is 8 hexadecimal characters.

Each chat record is stored as <CHAT_ID>.json and must contain:
CHAT_ID, CREATED_AT, PLATFORM_NATIVE_CHAT_ID, MODEL, FIRST_OBSERVED_NEXY_TEST_HEAD, STATUS.

A CHAT_ID is immutable for the lifetime of its chat session.
