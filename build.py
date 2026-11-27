# -*- coding: utf-8 -*-
"""生成 aheelv 统一入口主页。

数据来源：
  - 手工维护的站点 / 仓库 / 状态清单（下方常量）
  - data/sites.json（hello-world 数字资源中心的 78 条子页面）

产出：
  index.html                     静态渲染的完整主页（无 JS 亦可浏览）
  assets/portal/catalog.json     机器可读清单（便于批量核对与维护）
  assets/portal/style.css        样式（独立文件，由 style.css 源写入）
  assets/portal/app.js           渐进增强脚本
"""
import json
import html
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT
DATA = ROOT / "data" / "sites.json"

GENERATED_AT = "2026-11-27"
GH = "https://github.com/aheelv"
PAGES = "https://aheelv.github.io"

# ---------------------------------------------------------------------------
# 1. 六个在线 GitHub Pages 站点
# ---------------------------------------------------------------------------
SITES = [
    {
        "id": "hub",
        "name": "数字资源中心",
        "sub": "hello-world",
        "url": f"{PAGES}/hello-world/",
        "repo": f"{GH}/hello-world",
        "desc": "统一门户，12 大分类、78 个页面：教学建设、交互课件、科研支持、职称评审、书库藏书、科研写作教程等，全部离线可用。",
        "tags": ["门户", "教学", "科研", "78 页"],
        "icon": "grid",
        "accent": "indigo",
        "status": "ok",
        "featured": True,
    },
    {
        "id": "wps",
        "name": "计算机二级 WPS 培训站",
        "sub": "wps_2_test_learn",
        "url": f"{PAGES}/wps_2_test_learn/",
        "repo": f"{GH}/wps_2_test_learn",
        "desc": "大连财经学院校内教学资料：11 次课 44 课时、72 道实操题、781 道理论题、122 节点知识图谱与模拟考试系统。",
        "tags": ["教学", "考试", "WPS", "题库"],
        "icon": "book",
        "accent": "teal",
        "status": "ok",
        "featured": True,
    },
    {
        "id": "course",
        "name": "AI 工具应用实践课程",
        "sub": "maxhub",
        "url": f"{PAGES}/maxhub/",
        "repo": f"{GH}/maxhub",
        "desc": "32 课时 16 次课完整课程门户：课件、教学大纲、逐课练习资源、AI 应用实践案例与教材，零外部依赖。",
        "tags": ["课程", "AI", "实践", "16 课"],
        "icon": "terminal",
        "accent": "amber",
        "status": "ok",
        "featured": True,
    },
    {
        "id": "game",
        "name": "星集游戏舱",
        "sub": "game",
        "url": f"{PAGES}/game/",
        "repo": f"{GH}/game",
        "desc": "20 款零依赖单页小游戏，支持开始/暂停/重开/计分与难度选择，附参数化提示词生成器，便于二次创作。",
        "tags": ["游戏", "前端", "零依赖", "20 款"],
        "icon": "game",
        "accent": "rose",
        "status": "ok",
        "featured": True,
    },
    {
        "id": "genealogy",
        "name": "孙氏族谱",
        "sub": "sun-clan-genealogy",
        "url": f"{PAGES}/sun-clan-genealogy/",
        "repo": f"{GH}/sun-clan-genealogy",
        "desc": "1,752 人族谱静态站：SVG 世系树与血缘图、三层校验体系、角色权限治理，原生 ES Modules，零构建。",
        "tags": ["族谱", "可视化", "数据", "零构建"],
        "icon": "tree",
        "accent": "violet",
        "status": "ok",
        "featured": False,
    },
    {
        "id": "micro",
        "name": "AI 技术应用微专业",
        "sub": "ai",
        "url": f"{PAGES}/ai/",
        "repo": f"{GH}/ai",
        "desc": "微专业建设成果发布：课程管理站、6 门课程教学大纲汇编、6 份建设专题报告（179 页截图）三个子站。",
        "tags": ["教学", "AI", "微专业", "成果"],
        "icon": "layers",
        "accent": "sky",
        "status": "ok",
        "featured": False,
    },
]

# ---------------------------------------------------------------------------
# 2. 可访问的公开仓库（含无 Pages 的仓库）
# ---------------------------------------------------------------------------
REPOS = [
    {"name": "hello-world", "desc": "数字资源中心源码：门户 + 全部挂载子页，Simple.css 基底，零构建。",
     "lang": "HTML", "pushed": "2026-11-21", "stars": 0, "url": f"{GH}/hello-world",
     "site": f"{PAGES}/hello-world/", "status": "ok"},
    {"name": "wps_2_test_learn", "desc": "计算机二级 WPS 考试培训资料与练习素材生成器。",
     "lang": "HTML", "pushed": "2026-11-27", "stars": 0, "url": f"{GH}/wps_2_test_learn",
     "site": f"{PAGES}/wps_2_test_learn/", "status": "ok"},
    {"name": "game", "desc": "20 款小游戏与提示词生成器，纯前端无依赖。",
     "lang": "JavaScript", "pushed": "2026-11-24", "stars": 0, "url": f"{GH}/game",
     "site": f"{PAGES}/game/", "status": "ok"},
    {"name": "maxhub", "desc": "AI 工具应用实践课程，Pages 发布根为 docs/。",
     "lang": "HTML", "pushed": "2026-11-10", "stars": 0, "url": f"{GH}/maxhub",
     "site": f"{PAGES}/maxhub/", "status": "ok"},
    {"name": "ai", "desc": "人工智能技术应用微专业建设成果，三个同级静态子站。",
     "lang": "HTML", "pushed": "2026-11-16", "stars": 0, "url": f"{GH}/ai",
     "site": f"{PAGES}/ai/", "status": "ok"},
    {"name": "sun-clan-genealogy", "desc": "孙氏族谱数据建模与可视化站点。",
     "lang": "JavaScript", "pushed": "2026-09-25", "stars": 0, "url": f"{GH}/sun-clan-genealogy",
     "site": f"{PAGES}/sun-clan-genealogy/", "status": "ok"},
    {"name": "JavaMicroservicewithSpringXVMHM", "desc": "2019 年 IBM Bluemix 工具链生成的 Java 微服务示例（历史项目）。",
     "lang": "HTML", "pushed": "2019-05-31", "stars": 0, "url": f"{GH}/JavaMicroservicewithSpringXVMHM",
     "site": None, "status": "nopages"},
]

# ---------------------------------------------------------------------------
# 3. 失效 / 不可公开访问项
# ---------------------------------------------------------------------------
ISSUES = [
    {"name": "站点根地址", "url": f"{PAGES}/", "repo": f"{GH}/aheelv.github.io",
     "reason": "仓库已恢复 Public，但 GitHub Pages 功能尚未启用（has_pages = false），当前仍返回 HTTP 404。",
     "action": "到仓库 Settings → Pages → Build and deployment，Source 选 Deploy from a branch，Branch 选 main / (root) 并保存，即可发布本页。",
     "code": "404"},
    {"name": "JavaMicroservice 站点", "url": f"{PAGES}/JavaMicroservicewithSpringXVMHM/",
     "repo": f"{GH}/JavaMicroservicewithSpringXVMHM",
     "reason": "仓库未启用 GitHub Pages（has_pages = false），访问返回 HTTP 404。",
     "action": "仅保留源码仓库链接，站点地址不可用。", "code": "404"},
    {"name": "aheelv.github.io（仓库）", "url": f"{GH}/aheelv.github.io", "repo": None,
     "reason": "仓库为 Private，未登录访客无法访问。",
     "action": "如需公开请先调整仓库可见性。", "code": "私有"},
    {"name": "ijpr-agentic-supply-chain", "url": f"{GH}/ijpr-agentic-supply-chain", "repo": None,
     "reason": "私有仓库，未登录访客无法访问。", "action": "无公开链接。", "code": "私有"},
    {"name": "-AI---", "url": f"{GH}/-AI---", "repo": None,
     "reason": "私有仓库（智选云 AI 电商系统），未登录访客无法访问。", "action": "无公开链接。", "code": "私有"},
    {"name": "---1", "url": f"{GH}/---1", "repo": None,
     "reason": "私有空仓库，未登录访客无法访问。", "action": "无公开链接。", "code": "私有"},
]

LANG_COLOR = {
    "HTML": "#e34c26", "JavaScript": "#f1e05a", "Python": "#3572A5",
    "TypeScript": "#3178c6", "SCSS": "#c6538c", "Other": "#8b949e",
}


def esc(s):
    return html.escape(str(s), quote=True)


def icon_svg(kind):
    paths = {
        "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
        "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
        "terminal": '<polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>',
        "game": '<rect x="2" y="7" width="20" height="12" rx="4"/><line x1="7" y1="12" x2="11" y2="12"/><line x1="9" y1="10" x2="9" y2="14"/><circle cx="16" cy="11" r="1"/><circle cx="18.5" cy="14" r="1"/>',
        "tree": '<circle cx="12" cy="4" r="2"/><circle cx="6" cy="12" r="2"/><circle cx="18" cy="12" r="2"/><circle cx="12" cy="20" r="2"/><path d="M12 6v2M12 8H6v2M12 8h6v2M6 14v1a4 4 0 0 0 4 4h0M18 14v1a4 4 0 0 1-4 4h0"/>',
        "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 12 12 17 22 12"/><polyline points="2 17 12 22 22 17"/>',
    }
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{paths.get(kind, paths["grid"])}</svg>'


def build():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    items = data["items"]
    groups = data["groups"]
    extra_sites = data.get("sites", [])

    group_map = {g["id"]: g for g in groups}
    # 按分组聚合条目
    by_group = {}
    for it in items:
        by_group.setdefault(it["group"], []).append(it)

    # 机器可读清单
    catalog = {
        "owner": "aheelv",
        "site": "https://aheelv.github.io",
        "generated_at": GENERATED_AT,
        "sites": SITES,
        "pages": items,
        "extra_sites": extra_sites,
        "repos": REPOS,
        "issues": ISSUES,
    }
    cat_dir = OUT / "assets" / "portal"
    cat_dir.mkdir(parents=True, exist_ok=True)
    (cat_dir / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

    total_pages = len(items) + len(extra_sites)
    ok_links = len(SITES) + len(items) + len(extra_sites) + len([r for r in REPOS if r["site"]])
    html_parts = []
    A = html_parts.append

    A('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#4f46e5">
<title>aheelv · 数字资源总入口</title>
<meta name="description" content="GitHub 账号 aheelv 的公开站点与项目统一入口：6 个在线 GitHub Pages 站点、78 个可访问页面、7 个公开仓库，含状态核查与失效标记。">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='22' fill='%234f46e5'/><text x='50' y='70' font-size='58' text-anchor='middle' fill='white' font-family='Arial' font-weight='bold'>a</text></svg>">
<link rel="stylesheet" href="assets/portal/style.css">
</head>
<body>
<a class="skip-link" href="#main">跳到主要内容</a>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="#top" aria-label="返回顶部">
      <span class="brand-mark">a</span>
      <span class="brand-name">aheelv<span class="brand-dot">.</span><span class="brand-tail">dev</span></span>
    </a>
    <nav class="topnav" aria-label="主导航">
      <a href="#sites">在线站点</a>
      <a href="#resources">资源中心</a>
      <a href="#repos">代码仓库</a>
      <a href="#status">链接状态</a>
    </nav>
    <div class="topbar-actions">
      <button class="icon-btn" id="themeToggle" type="button" aria-label="切换深浅主题" title="切换主题">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
      </button>
      <a class="icon-btn" href="https://github.com/aheelv" target="_blank" rel="noopener noreferrer" aria-label="GitHub 主页" title="GitHub 主页">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.58 2 12.23c0 4.52 2.87 8.35 6.84 9.71.5.1.68-.22.68-.49v-1.7c-2.78.62-3.37-1.37-3.37-1.37-.45-1.18-1.11-1.49-1.11-1.49-.91-.64.07-.63.07-.63 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.35 1.12 2.92.86.09-.66.35-1.12.63-1.38-2.22-.26-4.55-1.14-4.55-5.05 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.71 0 0 .84-.28 2.75 1.05a9.3 9.3 0 0 1 5 0c1.91-1.33 2.75-1.05 2.75-1.05.55 1.41.2 2.45.1 2.71.64.72 1.03 1.63 1.03 2.75 0 3.92-2.34 4.78-4.57 5.03.36.32.68.94.68 1.9v2.82c0 .27.18.6.69.49A10.14 10.14 0 0 0 22 12.23C22 6.58 17.52 2 12 2z"/></svg>
      </a>
      <button class="menu-btn" id="menuToggle" type="button" aria-label="展开导航" aria-expanded="false">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
</header>

<main id="main">
<section class="hero" id="top">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="container hero-inner">
    <span class="eyebrow">GITHUB PAGES · UNIFIED ENTRY</span>
    <h1>一个入口，<span>抵达全部</span></h1>
    <p class="hero-lead">汇总账号 <strong>aheelv</strong> 名下所有可访问的 GitHub Pages 站点与公开仓库。每个条目都标注名称、说明、分类与可访问状态，链接逐条核验。</p>
    <div class="hero-stats">
      <div class="stat"><b>6</b><span>在线站点</span></div>
      <div class="stat"><b>''' + str(total_pages) + '''</b><span>可访问页面</span></div>
      <div class="stat"><b>7</b><span>公开仓库</span></div>
      <div class="stat"><b>''' + str(len(ISSUES)) + '''</b><span>状态标记</span></div>
    </div>
    <div class="hero-actions">
      <a class="btn btn-primary" href="#sites">浏览在线站点 <span aria-hidden="true">→</span></a>
      <a class="btn btn-ghost" href="#status">查看链接状态</a>
    </div>
  </div>
</section>

<div class="toolbar-wrap">
  <div class="container toolbar">
    <div class="search-box">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="searchInput" type="search" placeholder="搜索站点、页面、标签或路径…" aria-label="搜索所有条目" autocomplete="off">
      <kbd>/</kbd>
    </div>
    <div class="filter-group" role="group" aria-label="状态筛选">
      <button class="chip active" data-filter="all" type="button">全部</button>
      <button class="chip" data-filter="ok" type="button">可访问</button>
      <button class="chip" data-filter="issue" type="button">失效 / 私有</button>
    </div>
    <span class="result-count" id="resultCount" aria-live="polite"></span>
  </div>
</div>

<div class="container">

<!-- ============ 在线站点 ============ -->
<section class="section" id="sites">
  <div class="section-head">
    <div>
      <span class="section-no">01 / SITES</span>
      <h2>在线 GitHub Pages 站点</h2>
      <p>6 个站点均已通过 HTTP 200 核验。点击标题打开站点，「源码」直达对应仓库。</p>
    </div>
    <span class="section-count">6 个站点</span>
  </div>
  <div class="site-grid">
''')

    for s in SITES:
        search = " ".join([s["name"], s["sub"], s["desc"]] + s["tags"]).lower()
        tag_html = "".join(f'<span class="tag">{esc(t)}</span>' for t in s["tags"])
        A(f'''    <article class="site-card accent-{esc(s['accent'])}" data-status="ok" data-search="{esc(search)}">
      <div class="site-card-top">
        <span class="site-icon">{icon_svg(s['icon'])}</span>
        <span class="badge badge-ok"><span class="dot"></span>可访问</span>
      </div>
      <h3><a href="{esc(s['url'])}" target="_blank" rel="noopener noreferrer">{esc(s['name'])} <span class="ext" aria-hidden="true">↗</span></a></h3>
      <span class="site-sub">{esc(s['sub'])}</span>
      <p class="desc">{esc(s['desc'])}</p>
      <div class="tags">{tag_html}</div>
      <div class="card-foot">
        <a class="btn btn-sm" href="{esc(s['url'])}" target="_blank" rel="noopener noreferrer">打开站点 <span aria-hidden="true">→</span></a>
        <a class="text-link" href="{esc(s['repo'])}" target="_blank" rel="noopener noreferrer">源码 ↗</a>
      </div>
    </article>
''')

    A('''  </div>
</section>

<!-- ============ 资源中心 ============ -->
<section class="section" id="resources">
  <div class="section-head">
    <div>
      <span class="section-no">02 / PAGES</span>
      <h2>数字资源中心 · 全部页面</h2>
      <p>来自 <a class="inline-link" href="https://aheelv.github.io/hello-world/" target="_blank" rel="noopener noreferrer">hello-world</a> 站点的全部子页面，按 12 个主题分组，链接已逐条核验为 HTTP 200。</p>
    </div>
    <span class="section-count">''' + str(len(items)) + ''' 个页面</span>
  </div>
  <nav class="groupnav" aria-label="资源分类导航">
''')
    A('      <a href="#g-all" class="gpill">全部</a>')
    for g in groups:
        cnt = len(by_group.get(g["id"], []))
        A(f'      <a href="#g-{esc(g["id"])}" class="gpill">{esc(g["name"])} <span>{cnt}</span></a>')
    A('''  </nav>
''')

    for g in groups:
        gid = g["id"]
        glist = by_group.get(gid, [])
        if not glist:
            continue
        A(f'''  <div class="pgroup" id="g-{esc(gid)}">
    <div class="pgroup-head">
      <span class="pgroup-no">{esc(g['no'])}</span>
      <div>
        <h3>{esc(g['name'])}</h3>
        <p>{esc(g['desc'])}</p>
      </div>
      <span class="pgroup-count">{len(glist)} 页</span>
    </div>
    <div class="pgrid">
''')
        for it in glist:
            full = f"{PAGES}/hello-world/{it['url']}"
            search = " ".join([it["name"], it["desc"], it.get("groupName", "")] + it.get("tags", []) + [it["url"]]).lower()
            badge = ' <span class="mini-badge">首页入口</span>' if it.get("featured") else ""
            tag_html = "".join(f'<span class="tag">{esc(t)}</span>' for t in it.get("tags", []))
            A(f'''      <article class="pcard" data-status="ok" data-search="{esc(search)}">
        <h4>{esc(it['name'])}{badge}</h4>
        <p class="desc">{esc(it['desc'])}</p>
        <div class="tags">{tag_html}</div>
        <a class="pbtn" href="{esc(full)}" target="_blank" rel="noopener noreferrer">打开页面 <span aria-hidden="true">→</span></a>
        <span class="path">{esc(it['url'])}</span>
      </article>
''')
        A('    </div>\n  </div>\n')

    # extra sites
    if extra_sites:
        A('''  <div class="pgroup" id="g-extra">
    <div class="pgroup-head">
      <span class="pgroup-no">13</span>
      <div><h3>更多站点</h3><p>资源中心内另行登记的完整站点入口。</p></div>
      <span class="pgroup-count">''' + str(len(extra_sites)) + ''' 个</span>
    </div>
    <div class="pgrid">
''')
        for it in extra_sites:
            full = f"{PAGES}/hello-world/{it['path']}"
            search = " ".join([it["title"], it["desc"], it.get("group", "")] + it.get("tags", []) + [it["path"]]).lower()
            tag_html = "".join(f'<span class="tag">{esc(t)}</span>' for t in it.get("tags", []))
            A(f'''      <article class="pcard" data-status="ok" data-search="{esc(search)}">
        <h4>{esc(it['title'])}</h4>
        <p class="desc">{esc(it['desc'])}</p>
        <div class="tags">{tag_html}</div>
        <a class="pbtn" href="{esc(full)}" target="_blank" rel="noopener noreferrer">打开页面 <span aria-hidden="true">→</span></a>
        <span class="path">{esc(it['path'])}</span>
      </article>
''')
        A('    </div>\n  </div>\n')

    A('''</section>

<!-- ============ 代码仓库 ============ -->
<section class="section" id="repos">
  <div class="section-head">
    <div>
      <span class="section-no">03 / REPOS</span>
      <h2>可访问的公开仓库</h2>
      <p>7 个公开仓库均可直接访问；其中 6 个已启用 Pages，「源码 / 站点」双入口。</p>
    </div>
    <span class="section-count">7 个仓库</span>
  </div>
  <div class="repo-table" role="table" aria-label="公开仓库列表">
    <div class="repo-row repo-head" role="row">
      <span role="columnheader">仓库</span><span role="columnheader">语言</span>
      <span role="columnheader">最近更新</span><span role="columnheader">入口</span>
    </div>
''')
    for r in REPOS:
        st = "ok" if r["site"] else "nopages"
        search = " ".join([r["name"], r["desc"], r["lang"]]).lower()
        site_cell = f'<a class="text-link" href="{esc(r["site"])}" target="_blank" rel="noopener noreferrer">站点 ↗</a>' if r["site"] else '<span class="muted">无 Pages</span>'
        A(f'''    <div class="repo-row" role="row" data-status="{st}" data-search="{esc(search)}">
      <span class="repo-name" role="cell"><a href="{esc(r['url'])}" target="_blank" rel="noopener noreferrer">{esc(r['name'])} ↗</a><small>{esc(r['desc'])}</small></span>
      <span role="cell"><span class="lang"><i style="background:{LANG_COLOR.get(r['lang'], '#8b949e')}"></i>{esc(r['lang'])}</span></span>
      <span role="cell" class="muted">{esc(r['pushed'])}</span>
      <span role="cell" class="repo-links">{site_cell}</span>
    </div>
''')
    A('''  </div>
</section>

<!-- ============ 状态 ============ -->
<section class="section" id="status">
  <div class="section-head">
    <div>
      <span class="section-no">04 / STATUS</span>
      <h2>链接状态与失效标记</h2>
      <p>核验时间：''' + GENERATED_AT + '''。以下条目无法公开访问，均已明确标注原因与处理方式。</p>
    </div>
    <span class="section-count">''' + str(len(ISSUES)) + ''' 条标记</span>
  </div>
  <div class="issue-list">
''')
    for x in ISSUES:
        search = " ".join([x["name"], x["reason"], x["action"], x["code"]]).lower()
        link = f'<a href="{esc(x["url"])}" target="_blank" rel="noopener noreferrer">{esc(x["url"])} ↗</a>' if x["code"] != "私有" else f'<span class="broken-url">{esc(x["url"])}</span>'
        A(f'''    <article class="issue" data-status="issue" data-search="{esc(search)}">
      <span class="issue-code {'code-404' if x['code'] == '404' else 'code-private'}">{esc(x['code'])}</span>
      <div class="issue-body">
        <h3>{esc(x['name'])}</h3>
        <div class="issue-url">{link}</div>
        <p><b>原因：</b>{esc(x['reason'])}</p>
        <p><b>处理：</b>{esc(x['action'])}</p>
      </div>
    </article>
''')
    A('''  </div>
  <div class="notice">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v5M12 16h.01"/></svg>
    <p><b>关于根地址：</b>本页面已写入 <code>aheelv/aheelv.github.io</code> 仓库并已设为 Public。但 GitHub Pages 功能尚未启用（Settings → Pages → Source 选择 Deploy from a branch → main / (root)），启用后 <code>https://aheelv.github.io/</code> 即会显示此页。</p>
  </div>
</section>

</div>
</main>

<footer class="footer">
  <div class="container footer-inner">
    <div>
      <a class="brand" href="#top"><span class="brand-mark">a</span><span class="brand-name">aheelv<span class="brand-dot">.</span><span class="brand-tail">dev</span></span></a>
      <p>统一入口 · 链接核验于 ''' + GENERATED_AT + ''' · 静态生成，零外部依赖</p>
    </div>
    <div class="footer-links">
      <a href="https://github.com/aheelv" target="_blank" rel="noopener noreferrer">GitHub</a>
      <a href="#resources">资源中心</a>
      <a href="#status">状态</a>
      <a href="assets/portal/catalog.json" target="_blank" rel="noopener noreferrer">数据清单 JSON</a>
    </div>
  </div>
  <div class="container footer-note">设计参考：Academic Pages（MIT，17.8k ★）与 Simple.css（MIT）。全部条目来源于 GitHub API 与逐条 HTTP 核验。</div>
</footer>

<button class="to-top" id="toTop" type="button" aria-label="返回顶部" title="返回顶部">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>

<script src="assets/portal/app.js"></script>
</body>
</html>
''')

    (OUT / "index.html").write_text("".join(html_parts), encoding="utf-8")
    print(f"sites={len(SITES)} pages={len(items)} extra={len(extra_sites)} repos={len(REPOS)} issues={len(ISSUES)}")
    print(f"index.html bytes={len((OUT/'index.html').read_bytes())}")


if __name__ == "__main__":
    build()
