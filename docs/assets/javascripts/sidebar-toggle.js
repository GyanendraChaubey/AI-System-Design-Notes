(function () {
  var NAV_KEY = 'ai-nav-collapsed';
  var TOC_KEY = 'ai-toc-collapsed';

  var NAV_ARROW_OPEN  = 'M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z';
  var TOC_ARROW_OPEN  = 'M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z';

  function makeSvg(path) {
    return '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">'
      + '<path fill="currentColor" d="' + path + '"/></svg>';
  }

  function makeBtn(cls, title, svgPath) {
    var btn = document.createElement('button');
    btn.className   = 'sidebar-toggle ' + cls;
    btn.title       = title;
    btn.innerHTML   = makeSvg(svgPath);
    return btn;
  }

  function init() {
    var body = document.body;

    // Restore persisted state before first paint (avoids layout flash)
    if (localStorage.getItem(NAV_KEY)) body.classList.add(NAV_KEY);
    if (localStorage.getItem(TOC_KEY)) body.classList.add(TOC_KEY);

    // Guard against double-inject on instant-nav pages
    if (document.querySelector('.sidebar-toggle--nav')) return;

    var hasNav = document.querySelector('.md-sidebar--primary');
    if (hasNav) {
      var navBtn = makeBtn('sidebar-toggle--nav', 'Toggle navigation', NAV_ARROW_OPEN);
      navBtn.addEventListener('click', function () {
        var col = body.classList.toggle(NAV_KEY);
        localStorage.setItem(NAV_KEY, col ? '1' : '');
      });
      document.body.appendChild(navBtn);
    }

    var hasToc = document.querySelector('.md-sidebar--secondary');
    if (hasToc) {
      var tocBtn = makeBtn('sidebar-toggle--toc', 'Toggle table of contents', TOC_ARROW_OPEN);
      tocBtn.addEventListener('click', function () {
        var col = body.classList.toggle(TOC_KEY);
        localStorage.setItem(TOC_KEY, col ? '1' : '');
      });
      document.body.appendChild(tocBtn);
    }
  }

  // Initial page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // MkDocs Material instant navigation — content swaps but <body> persists,
  // so only re-inject if the buttons disappeared for some reason.
  document.addEventListener('DOMContentSwitch', init);
})();
