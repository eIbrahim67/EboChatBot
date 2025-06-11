from marshmallow import Schema, fields as ma_fields


class ChatInputSchema(Schema):
    session_id = ma_fields.String(required=False, allow_none=True)
    input = ma_fields.String(required=True)
