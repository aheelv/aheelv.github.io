/* aheelv 统一入口 · 渐进增强
   页面在禁用 JS 时仍可完整浏览与跳转；本脚本仅提供搜索、筛选、主题、计数与导航高亮。 */
(function () {
  'use strict';

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ---------- 主题 ---------- */
  var root = document.documentElement;
  var stored;
  try { stored = localStorage.getItem('aheelv-theme'); } catch (e) { stored = null; }
  if (stored === 'dark' || stored === 'light') {
    root.setAttribute('data-theme', stored);
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    root.setAttribute('data-theme', 'dark');
  }
  var themeBtn = $('#themeToggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('aheelv-theme', next); } catch (e) {}
    });
  }

  /* ---------- 移动端导航 ---------- */
  var menuBtn = $('#menuToggle');
  var topnav = $('.topnav');
  if (menuBtn && topnav) {
    menuBtn.addEventListener('click', function () {
      var open = topnav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', String(open));
    });
    $$('a', topnav).forEach(function (a) {
      a.addEventListener('click', function () {
        topnav.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- 搜索与筛选 ---------- */
  var input = $('#searchInput');
  var chips = $$('.chip[data-filter]');
  var countEl = $('#resultCount');
  var entries = $$('[data-search]');
  var sections = $$('.section');
  var groups = $$('.pgroup');
  var currentFilter = 'all';
  var noResult = null;

  function total() { return entries.length; }

  function apply() {
    var q = (input && input.value || '').trim().toLowerCase();
    var terms = q.split(/\s+/).filter(Boolean);
    var visible = 0;

    entries.forEach(function (el) {
      var hay = el.getAttribute('data-search') || '';
      var status = el.getAttribute('data-status') || 'ok';
      var textOk = terms.every(function (t) { return hay.indexOf(t) !== -1; });
      var filterOk = currentFilter === 'all' ||
        (currentFilter === 'ok' && status === 'ok') ||
        (currentFilter === 'issue' && status === 'issue');
      var show = textOk && filterOk;
      el.hidden = !show;
      if (show) visible++;
    });

    // 分组：组内无可见条目则整组隐藏
    groups.forEach(function (g) {
      var cards = $$('[data-search]', g);
      var any = cards.some(function (c) { return !c.hidden; });
      g.hidden = !any;
    });
    // 站点网格 / 仓库表 / 状态列表：整块无可见条目则隐藏其容器
    sections.forEach(function (s) {
      var cards = $$('[data-search]', s);
      if (!cards.length) return;
      var any = cards.some(function (c) { return !c.hidden; });
      var head = $('.section-head', s);
      if (head) head.hidden = !any;
      var grid = $('.site-grid, .repo-table, .issue-list, .groupnav', s);
      if (grid) grid.hidden = !any;
    });

    document.body.classList.toggle('searching', !!(q || currentFilter !== 'all'));

    if (countEl) {
      countEl.textContent = (q || currentFilter !== 'all')
        ? '显示 ' + visible + ' / ' + total() + ' 条'
        : total() + ' 条已核验条目';
    }

    // 空结果提示
    if (visible === 0 && !noResult) {
      noResult = document.createElement('div');
      noResult.className = 'no-result';
      noResult.innerHTML = '<b>没有匹配的条目</b>试试其他关键词，或切换筛选条件。';
      var main = $('#main');
      if (main) main.appendChild(noResult);
    } else if (visible > 0 && noResult) {
      noResult.remove();
      noResult = null;
    }
  }

  if (input) {
    input.addEventListener('input', apply);
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== input &&
          !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) {
        e.preventDefault();
        input.focus();
      }
      if (e.key === 'Escape' && document.activeElement === input) {
        input.value = '';
        apply();
        input.blur();
      }
    });
  }

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      currentFilter = chip.getAttribute('data-filter') || 'all';
      chips.forEach(function (c) { c.classList.toggle('active', c === chip); });
      apply();
    });
  });
  apply();

  /* ---------- 返回顶部 ---------- */
  var toTop = $('#toTop');
  if (toTop) {
    var onScroll = function () {
      toTop.classList.toggle('show', window.scrollY > 480);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- 导航高亮 ---------- */
  if ('IntersectionObserver' in window) {
    var links = $$('.topnav a');
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = en.target.id;
        links.forEach(function (a) {
          a.classList.toggle('active', a.getAttribute('href') === '#' + id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { if (s.id) observer.observe(s); });
  }
})();
