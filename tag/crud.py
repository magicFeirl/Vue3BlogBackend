from .schema import Tag, TagOut, ArticleTag
from typing import List


async def create_tag(tag_name: str):
    return await Tag.get_or_create(tag_name=tag_name)


async def get_tag_info(tag_name: str) -> TagOut:
    return await TagOut.from_queryset_single(Tag.get_or_none(tag_name=tag_name))


async def add_tags_to_article(article_id: str, tags: List[str]):
    for tag in tags:
        tag_info, _ = await create_tag(tag_name=tag)  # tag 不存在就创建
        await ArticleTag.create(article_id=article_id, tag_id=tag_info.tag_id)
