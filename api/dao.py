from .database_util import * # init db
from datetime import datetime
from bson import ObjectId
from mongoengine import (
    Document, DynamicDocument,
    EmbeddedDocument,
    StringField,
    BooleanField,
    EmailField,
    ListField,
    DictField,
    DateTimeField,
    IntField,
    FloatField,
    ObjectIdField,
    EmbeddedDocumentField
)
from typing import List

class Personalization(EmbeddedDocument):
    id = ObjectIdField(db_field="_id", default=ObjectId)
    memories = BooleanField(default=True)


class User(Document):
    meta = {
        "collection": "users",
        "strict": False,
    }

    # MongoDB 的 _id 会自动映射为 User.id
    name = StringField(required=True)
    username = StringField(required=True)
    email = EmailField(required=True)

    email_verified = BooleanField(
        db_field="emailVerified",
        default=False
    )

    password = StringField(required=True)

    avatar = StringField(null=True)

    provider = StringField(
        default="local",
    )

    role = StringField(
        default="USER",
        choices=["USER", "ADMIN"]
    )

    plugins = ListField(default=list)

    two_factor_enabled = BooleanField(
        db_field="twoFactorEnabled",
        default=False
    )

    terms_accepted = BooleanField(
        db_field="termsAccepted",
        default=False
    )

    personalization = EmbeddedDocumentField(
        Personalization,
        default=Personalization
    )

    backup_codes = ListField(
        db_field="backupCodes",
        default=list
    )

    refresh_token = ListField(
        db_field="refreshToken",
        default=list
    )

    favorites = ListField(default=list)

    skill_states = DictField(
        db_field="skillStates",
        default=dict
    )

    created_at = DateTimeField(
        db_field="createdAt",
        default=datetime.utcnow
    )

    updated_at = DateTimeField(
        db_field="updatedAt",
        default=datetime.utcnow
    )

    version = IntField(
        db_field="__v",
        default=0
    )

    def __str__(self):
        return str(self.to_mongo().to_dict())

class Balance(Document):
    meta = {
        "collection": "balances",
        "strict": False
    }

    user = ObjectIdField(required=True)

    auto_refill_enabled = BooleanField(
        db_field="autoRefillEnabled",
        default=False
    )

    last_refill = DateTimeField(
        db_field="lastRefill"
    )

    refill_amount = IntField(
        db_field="refillAmount",
        default=0
    )

    refill_interval_unit = StringField(
        db_field="refillIntervalUnit"
    )

    refill_interval_value = IntField(
        db_field="refillIntervalValue",
        default=0
    )

    token_credits = FloatField(
        db_field="tokenCredits",
        default=0
    )

    def __str__(self):
        return str(self.to_mongo().to_dict())