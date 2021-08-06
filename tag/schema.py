from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Tag(models.Model):
    """保存 Tag 相关信息和"""
    tag_id = fields.IntField(pk=True)
    tag_name = fields.CharField(max_length=15, index=True)
    created_at = fields.DatetimeField(auto_now=True)


class ArticleTag(models.Model):
    """关联文章和tag"""
    id = fields.IntField(pk=True)
    article_id = fields.IntField(index=True)
    tag_id = fields.IntField(index=True)


TagOut = pydantic_model_creator(Tag, name="TagOut")
