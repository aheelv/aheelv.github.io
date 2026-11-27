# aheelv 统一入口主页 · 维护说明

本目录是 `https://aheelv.github.io` 统一入口主页的**本地源文件**，与 GitHub 仓库 `aheelv/aheelv.github.io` 同步。

## 文件结构

| 文件 | 作用 |
| --- | --- |
| `build.py` | 静态页生成器。修改数据后运行 `python build.py` 重新生成 `index.html` |
| `index.html` | 生成的完整主页（静态渲染，禁用 JS 亦可浏览全部条目） |
| `assets/portal/style.css` | 样式（浅色/深色主题、响应式栅格） |
| `assets/portal/app.js` | 渐进增强：搜索、状态筛选、主题切换、导航高亮、返回顶部 |
| `assets/portal/catalog.json` | 机器可读的条目清单（站点 / 页面 / 仓库 / 状态） |
| `data/sites.json` | 数字资源中心 78 个子页面的源数据（来自 hello-world 仓库） |
| `data/link-status.json` | 78 个子页面链接的 HTTP 核验结果 |

## 数据来源与核验

- 账号与仓库信息：GitHub API（`aheelv` 的 11 个仓库，其中 7 个公开）
- 6 个在线 Pages 站点：HTTP 200 核验通过
- 78 个资源中心页面：并发 HTTP 核验，全部 200
- 失效/私有条目：6 条，均标注原因与处理方式（HTTP 404 与 Private）

## 日常维护

### 修改条目
1. **在线站点 / 仓库 / 失效标记**：编辑 `build.py` 顶部的 `SITES`、`REPOS`、`ISSUES` 常量。
2. **资源中心页面**：编辑 `data/sites.json`（结构与 hello-world 仓库 `assets/sites.json` 一致）。
3. 运行 `python build.py` 重新生成 `index.html`。
4. 将变更提交到 `aheelv/aheelv.github.io` 仓库的 `main` 分支。

### 新增页面
在 `data/sites.json` 的 `items` 数组中追加一条：
```json
{
  "group": "分组ID",
  "groupName": "分组名称",
  "name": "页面名称",
  "desc": "一句话说明",
  "url": "相对路径（相对 hello-world 站点根）",
  "tags": ["标签1", "标签2"],
  "featured": false
}
```
若新增分组，需同时在 `groups` 数组中登记。重新生成后，页面会自动进入对应分类并参与搜索。

### 链接状态更新
重新核验链接后，更新 `data/link-status.json` 与 `build.py` 中的 `ISSUES` 列表，并修正 `GENERATED_AT` 日期。

## 设计参考

- **Academic Pages**（`academicpages/academicpages.github.io`，17.8k ★，MIT）：学术化清晰版式、分类导航、卡片网格理念。
- **Simple.css**（MIT）：轻量、无框架的样式体系。

参考文件已下载至工作区 `references/academicpages-template/`（375 个文件）。

## 重要说明

`aheelv/aheelv.github.io` 仓库当前为 **Private**。GitHub 对私有仓库自动停用 Pages，因此根地址 `https://aheelv.github.io/` 返回 404。
要让新主页上线，需要在 GitHub 仓库设置中将该仓库改为 **Public**（Settings → General → Danger Zone → Change visibility）。
仓库可见性无法通过 API 修改，需账号所有者手动操作。
