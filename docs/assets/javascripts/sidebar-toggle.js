(function () {
  var NAV_KEY = 'ai-nav-collapsed';
  var TOC_KEY = 'ai-toc-collapsed';

  var NAV_SVG = '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"/></svg>';
  var TOC_SVG = '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/></svg>';

  function makeBtn(extraClass, title, svgHtml) {
    var btn = document.createElement('button');
    btn.className = 'sidebar-toggle ' + extraClass;
    btn.title = title;
    btn.innerHTML = svgHtml;
    return btn;
  }

  // Place the button flush against the inner edge of the sidebar
  function positionBtn(btn, sidebar, side) {
    if (!btn || !sidebar) return;
    // getBoundingClientRect gives the actual rendered width including padding
    var w = sidebar.getBoundingClientRect().width;
    btn.style[side] = w + 'px';
  }

  function updatePositions() {
    var navSidebar = document.querySelector('.md-sidebar--primary');
    var tocSidebar = document.querySelector('.md-sidebar--secondary');
    var navBtn    = document.querySelector('.sidebar-toggle--nav');
    var tocBtn    = document.querySelector('.sidebar-toggle--toc');
    var body      = document.body;

    // Only reposition when the sidebar is currently open
    if (navBtn && navSidebar && !body.classList.contains(NAV_KEY)) {
      positionBtn(navBtn, navSidebar, 'left');
    }
    if (tocBtn && tocSidebar && !body.classList.contains(TOC_KEY)) {
      positionBtn(tocBtn, tocSidebar, 'right');
    }
  }

  function init() {
    var body = document.body;

    // Restore saved preference immediately (before paint, avoids flash)
    if (localStorage.getItem(NAV_KEY) === '1') body.classList.add(NAV_KEY);
    if (localStorage.getItem(TOC_KEY) === '1') body.classList.add(TOC_KEY);

    // Don't double-inject on instant-nav page switches
    if (document.querySelector('.sidebar-toggle--nav')) {
      updatePositions();
      return;
    }

    var navSidebar = document.querySelector('.md-sidebar--primary');
    var tocSidebar = document.querySelector('.md-sidebar--secondary');

    if (navSidebar) {
      var navBtn = makeBtn('sidebar-toggle--nav', 'Collapse navigation', NAV_SVG);
      document.body.appendChild(navBtn);

      // Set initial position from real measured width
      positionBtn(navBtn, navSidebar, 'left');

      navBtn.addEventListener('click', function () {
        var collapsed = body.classList.toggle(NAV_KEY);
        localStorage.setItem(NAV_KEY, collapsed ? '1' : '');
        navBtn.title = collapsed ? 'Expand navigation' : 'Collapse navigation';
        if (!collapsed) {
          // Restore position after transition finishes
          setTimeout(function () { positionBtn(navBtn, navSidebar, 'left'); }, 280);
        }
      });
    }

    if (tocSidebar) {
      var tocBtn = makeBtn('sidebar-toggle--toc', 'Collapse table of contents', TOC_SVG);
      document.body.appendChild(tocBtn);

      positionBtn(tocBtn, tocSidebar, 'right');

      tocBtn.addEventListener('click', function () {
        var collapsed = body.classList.toggle(TOC_KEY);
        localStorage.setItem(TOC_KEY, collapsed ? '1' : '');
        tocBtn.title = collapsed ? 'Expand table of contents' : 'Collapse table of contents';
        if (!collapsed) {
          setTimeout(function () { positionBtn(tocBtn, tocSidebar, 'right'); }, 280);
        }
      });
    }

    // Re-measure on window resize (sidebar width can change)
    window.addEventListener('resize', updatePositions);
  }

  // Initial page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // MkDocs instant navigation — body persists, content swaps
  document.addEventListener('DOMContentSwitch', init);
})();
