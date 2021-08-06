from fastapi import APIRouter, Depends, HTTPException
from .schema import Tag, ArticleTag, TagOut
from article.schema import ArticleModel
from . import crud as tag_crud
from auth import get_current_user
from typing import List
from pydantic import BaseModel


from utils.params import query_param
from utils.responses import BaseResponse

router = APIRouter(prefix='/tag')


@router.get('/', response_model=BaseResponse)
async def get_tag_info(tag_id: str):
    return BaseResponse(code=200, message='获取 tag 信息成功', data=await Tag.get_or_none(tag_id=tag_id))

@router.get('/count')
async def get_tags_count():
    return {
        'code': 200,
        'message': '获取 tag 总数成功',
        'data': [],
        'count': await Tag.all().count()
    }

@router.get('/articles', response_model=BaseResponse)
async def get_articles(tag_id: str, q=Depends(query_param)):
    """获取某个 tags 下的所有 article 简要信息"""
    articles_id = await ArticleTag.filter(tag_id=tag_id).values_list('article_id', flat=True)

    data = (await ArticleModel.filter(id__in=articles_id).
            limit(q['limit']).
            offset(q['offset']).
            values(
        'id', 'title', 'created_at',
        'description', 'author_id'
    ))

    return BaseResponse(
        code=200,
        message='获取文章信息成功',
        data=data
    )


@router.get('/article', response_model=BaseResponse)
async def get_article_tags(article_id: str):
    """获取文章的 tags"""
    tags_id = await ArticleTag.filter(article_id=article_id).values_list('tag_id', flat=True)
    data = await TagOut.from_queryset(Tag.filter(tag_id__in=tags_id))

    return BaseResponse(
        code=200,
        message='获取文章 tags 成功',
        data=data
    )


class AddTagsTodArticle(BaseModel):
    article_id: str
    tags: List[str]


@router.post('/article', response_model=BaseResponse)
async def add_tag_to_article(data: AddTagsTodArticle, user=Depends(get_current_user)):
    if len(data.tags) > 5:
        raise HTTPException(403, {
            'code': 403,
            'message': 'tag 数不能多于 5 个'
        })

    """添加 tag 到指定文章"""
    await tag_crud.add_tags_to_article(data.article_id, data.tags)

    return BaseResponse(
        code=200,
        message='添加 tag 成功'
    )
