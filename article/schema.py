from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ArticleModel(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=128)
    description = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now=True)
    author_id = fields.IntField(index=True)


ArticleIn = pydantic_model_creator(
    ArticleModel, name="ArticleIn", exclude=('id', 'created_at', 'author_id'), exclude_readonly=True)
