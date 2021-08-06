## 简介

这是一个实现了

* 用户登录
* 用户注册
* 发表、删除、编辑博客
* 添加博客标签

的博客后端程序，使用 FastAPI + Tortoise-ORM 。

配合[Vue3Blog](https://github.com/magicFeirl/Vue3Blog)食用效果更佳。

## 配置

在项目根目录创建一个`.env`文件，内容如下:

```html
DB_URL= # Your database address, MySQL is recommended
```

## 运行

`docker-compose up -d`

需要预装 Docker 和 Docker-Compose