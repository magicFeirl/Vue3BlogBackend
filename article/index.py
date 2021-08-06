from auth import get_current_user
from typing import List
from fastapi import APIRouter, Depends
from .schema import ArticleModel, ArticleIn
from tag.crud import add_tags_to_article
from tag.schema import ArticleTag

from utils.responses import BaseResponse
from utils.params import query_param

router = APIRouter()


class ArticleInWithTags(ArticleIn):
    tags: List[str]


@router.post('/article', response_model=BaseResponse)
async def new_article(article: ArticleInWithTags, user=Depends(get_current_user)):
    # article_dict = article.dict()
    # article_dict['tags'] = None  # 删掉 tags 字段

    obj = await ArticleModel.create(**article.dict(), author_id=user['id'])

    await add_tags_to_article(article_id=obj.id, tags=article.tags)

    return BaseResponse(
        code=200,
        message='新建文章成功'
    )


@router.delete('/article', response_model=BaseResponse)
async def delete_article(id: str, user=Depends(get_current_user)):
    await ArticleModel.get(id=id).delete()
    await ArticleTag.filter(article_id=id).delete() # 连带删除文章的 tag 关联

    return BaseResponse(
        code=200,
        message='删除文章成功'
    )


@router.put('/article', response_model=BaseResponse)
async def update_article(id: str, article: ArticleIn, user=Depends(get_current_user)):
    await ArticleModel.get(id=id).update(**article.dict())

    return BaseResponse(
        code=200,
        message='更新文章成功'
    )


@router.get('/article', response_model=BaseResponse)
async def get_article(id: int):
    return BaseResponse(
        code=200,
        message='获取文章数据成功',
        data=await ArticleModel.get(id=id)
    )


@router.get('/articles')
async def get_all_articles(q=Depends(query_param)):
    data = await ArticleModel.all().limit(q['limit']).offset(q['offset']).values(
        'id', 'title', 'created_at',
        'description', 'author_id'
    )

    count = await ArticleModel.all().count()

    return {
        'code': 200,
        'message': '获取文章列表成功',
        'data': data,
        'count': count
    }

    # return BaseResponse(
    #     code=200,
    #     message='获取文章列表成功',
    #     data=data
    # )
