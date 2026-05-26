# Komic

**自托管漫画 / 本子服务器** — 支持目录、ZIP、7z、RAR 格式。

后端 FastAPI + SQLite，前端 Vue 3 + Vite + TailwindCSS，可选 WebDAV 访问。

## 功能特性

- **漫画扫描** — 扫描 `MANKA_PATH` 下的子目录/压缩包，自动识别格式并入库
- **封面与缩略图** — 自动提取第一张图片作为封面，支持缩略图尺寸调整
- **评分系统** — 0–5 星评分，支持按评分筛选
- **标签管理** — 为漫画添加/删除标签，按标签筛选
- **全文搜索** — 按标题模糊搜索
- **排序** — 按标题或修改时间升序/降序排列
- **阅读器** — 分页浏览漫画页面
- **WebDAV 访问** — 通过 WebDAV 协议浏览漫画目录、按评分/标签筛选、通过 MOVE 操作评分
- **双 UI** — 同时提供 HTMX 服务端渲染页面和 Vue 3 SPA 前端
- **后台扫描** — 扫描在后台线程执行，前端实时查看进度
- **Docker 支持** — 多阶段构建，开箱即用

## 快速开始

### Docker Compose（推荐）

```bash
docker compose up -d
# 访问 http://localhost:8000
```

### 本地开发

```bash
# 后端
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 前端（可选，默认使用预构建的 dist）
cd frontend
npm install
npm run dev
```

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `MANKA_PATH` | `/manka` | 漫画存放目录，Docker 中为只读 |
| `DB_PATH` | `/data/komic.db` | SQLite 数据库路径 |
| `DAV_PREFIX` | `/dav` | WebDAV 挂载路径 |
| `EXCLUDE_DIRS` | `""` | 扫描时跳过的目录名（逗号分隔） |

所有配置通过环境变量设置，不加载 `.env` 文件。

## 项目结构

```
├── app/                          # 后端 Python 源码
│   ├── main.py                   # FastAPI 入口，挂载路由/静态文件/WebDAV
│   ├── config.py                 # 环境变量配置
│   ├── database.py               # SQLite + SQLAlchemy，Alembic 迁移
│   ├── models.py                 # 数据模型（Comic, Tag）
│   ├── scanner.py                # 文件系统扫描逻辑
│   ├── scan_manager.py           # 后台扫描线程管理
│   ├── cover.py                  # 封面提取与缩放
│   ├── pages.py                  # 页面图片读取与缩放
│   ├── dav_provider.py           # WebDAV 虚拟文件系统
│   ├── routers/
│   │   ├── api.py                # REST API 路由
│   │   └── web.py                # HTMX 页面路由
│   ├── templates/                # Jinja2 模板
│   │   ├── index.html            # 主页面
│   │   ├── _comic_grid.html      # 漫画网格
│   │   └── _stars.html           # 星级评分组件
│   └── static/
│       └── app.css               # 样式
├── frontend/                     # Vue 3 SPA 前端
│   ├── index.html                # SPA 入口
│   ├── package.json              # 依赖：Vue 3, Pinia, Vite, TailwindCSS
│   ├── vite.config.js            # Vite 配置
│   ├── tailwind.config.js        # TailwindCSS 配置
│   ├── postcss.config.js         # PostCSS 配置
│   └── src/
│       ├── main.js               # 应用初始化
│       ├── App.vue               # 根组件
│       ├── style.css             # 全局样式
│       ├── api/index.js          # API 客户端
│       ├── stores/               # Pinia 状态管理
│       │   ├── comic.js          # 漫画数据 store
│       │   └── theme.js          # 主题 store
│       ├── composables/          # 组合式函数
│       │   └── useDebounce.js    # 防抖工具
│       └── components/           # Vue 组件
│           ├── AppHeader.vue     # 顶栏
│           ├── ComicCard.vue     # 漫画卡片
│           ├── ComicDetailModal.vue  # 漫画详情弹窗
│           ├── ComicGrid.vue     # 漫画网格
│           ├── Pagination.vue    # 分页
│           ├── ScanProgress.vue  # 扫描进度条
│           ├── SearchToolbar.vue # 搜索/筛选工具栏
│           └── StarRating.vue    # 星级评分组件
├── alembic/                      # 数据库迁移
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                 # 迁移版本
├── .github/workflows/
│   └── build-image.yml           # CI：构建并保存 Docker 镜像
├── requirements.txt              # Python 依赖
├── Dockerfile                    # 多阶段 Docker 构建
├── docker-compose.yml            # Docker Compose 配置
├── docker-compose_qnap.yml       # QNAP NAS 专用配置
├── alembic.ini                   # Alembic 配置
└── LICENSE
```

## 技术栈

### 后端
- **Python 3.12** + **FastAPI** — Web 框架
- **SQLite** + **SQLAlchemy 2.0** — 数据库与 ORM
- **Alembic** — 数据库迁移
- **Jinja2** — 服务端模板
- **HTMX** — 服务端渲染交互
- **WsgiDAV** — WebDAV 服务器
- **Pillow** — 图片处理
- **py7zr / rarfile / zipfile** — 压缩包支持
- **python-multipart** — 文件上传支持

### 前端
- **Vue 3** (Composition API) — UI 框架
- **Pinia** — 状态管理
- **Vite** — 构建工具
- **TailwindCSS** — 样式框架

### 基础设施
- **Docker** — 多阶段构建
- **GitHub Actions** — CI

## API 概览

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/api/comics` | 漫画列表（支持筛选/排序/分页/搜索） |
| `GET` | `/api/comics/{id}` | 漫画详情 |
| `GET` | `/api/comics/{id}/cover` | 漫画封面 |
| `GET` | `/api/comics/{id}/page/{n}` | 漫画页码图片 |
| `POST` | `/api/comics/{id}/rating?rating=N` | 设置评分 |
| `POST` | `/api/comics/{id}/tags` | 添加/删除标签 |
| `GET` | `/api/tags` | 标签列表 |
| `DELETE` | `/api/tags/{id}` | 删除标签 |
| `POST` | `/api/scan` | 触发重新扫描 |
| `GET` | `/api/scan/status` | 扫描状态 |
| `GET` | `/api/scan/progress-bar` | 扫描进度（HTMX） |

## WebDAV

WebDAV 通过 `MOVE` 操作实现评分机制：

- 将漫画文件 `MOVE` 到 `/dav/rating/{N}/...` 路径即可设置评分（N = 0–5）
- 虚拟目录结构：`/dav/all/`（全部漫画）、`/dav/rating/{N}/`（按评分）、`/dav/tag/{name}/`（按标签）
- 漫画目录下的图片文件可直接读取

## 数据库迁移

```bash
# 自动生成迁移
alembic revision --autogenerate -m "描述"

# 手动执行迁移
alembic upgrade head
```

迁移文件存放在 `alembic/versions/`，启动时自动执行 `alembic upgrade head`。

## 漫画格式

支持的漫画格式：

- **目录**（`dir`）— MANKA_PATH 下的子目录，内部为图片文件
- **ZIP**（`.zip`）
- **7z**（`.7z`）
- **RAR**（`.rar`）

文件名中的日期前缀（`YYYYMMDD`）会自动剥离，仅用于排序。封面使用目录或压缩包中的第一张图片（按文件名排序）。

## Docker 构建

```bash
docker build -t komic:latest .
docker compose up -d
```

构建分为两个阶段：
1. **frontend** — Node.js 20 Alpine，构建 Vue SPA
2. **runtime** — Python 3.12 slim，安装 libmagic1，复制后端代码及前端构建产物

CI（GitHub Actions）在 `main` 分支推送或发布 release 时自动构建，产物为 `komic.tar.gz`，可用于 QNAP Container Station 导入。
