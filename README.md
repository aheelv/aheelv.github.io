# aheelv.github.io · 人工智能工具应用实践课程门户

大连财经学院管理学院《人工智能工具应用实践》课程网站，由 GitHub Pages 静态托管。

**站点地址：** https://aheelv.github.io/

## 内容

| 路径 | 说明 |
| --- | --- |
| `index.html` | 课程首页（含 16 次课练习资源直达下载区） |
| `exercises.html` | 16 次课练习下载页：按模块筛选、搜索、整包或逐份下载 |
| `courseware.html` / `syllabus.html` / `modules.html` 等 | 课件中心、课程大纲、知识模块、案例、术语、趋势 |
| `downloads/` | 16 个单课 ZIP、全 16 课总包、总手册、资源清单与 188 份单课资料 |
| `practice/index.html` | 独立课堂练习资源站（16 课任务详情与逐份下载） |

练习题目均为单次课 70—100 分钟、学生单人独立完成、以 WorkBuddy 为主要工具的 AI 应用任务；每套含任务说明、背景资料、素材、分钟级操作步骤、成果要求、100 分评价量规与教师核验卡。素材全部为课堂虚构数据。

## 静态展示版的限制

GitHub Pages 不运行 Node.js 后端，因此以下功能在本站点不可用，页面会给出明确提示：

- 登录 / 注册 / 扫码登录、个人中心
- 选课意向、学习反馈的实时提交与统计
- 教师发布课程通知

这些页面仍可浏览，用于展示界面与课程内容。**完整交互版**请在本地运行：

```bash
cd site
node server.js
# 打开 http://localhost:3000
```

后端为纯 Node.js 内置模块实现，数据存于 `site/data/db.json`（未包含在静态发布版中）。

## 构建与维护

源文件位于课程项目仓库，`exercise-build/` 下提供可重复构建脚本：

```bash
python exercise-build/build.py          # 任务单、素材、16 个 ZIP、清单与元数据
python exercise-build/build_pages.py    # 两站网页与 site/downloads 同步
python exercise-build/verify_pages.py   # 链接、锚点、ZIP 完整性体检
python exercise-build/prepare_publish.py <输出目录>   # 生成静态发布版
```

发布版自动排除 `server.js`、`package.json` 与 `data/`，注入 `static-mode.js` 处理 `/api/*` 降级，并写入 `.nojekyll` 以保证中文文件名与 `.md` 资源按原样提供。
