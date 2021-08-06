from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class AuthModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    password_hash = fields.CharField(max_length=128)
    register_time = fields.DatetimeField(auto_now=True)


AuthIn = pydantic_model_creator(
    AuthModel, name='AuthIn', exclude_readonly=True)
AuthOut = pydantic_model_creator(AuthModel,
                                 name='AuthOut', include=('name', 'register_tiem'))
