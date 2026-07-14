// Mermaid emits every diagram as <svg width="100%" style="max-width:
// {natural-width}px">. The width="100%" attribute resolves against the
// reading column first, so wide diagrams get shrunk to fit it — and
// because SVG text scales with the whole graphic, that shrink is what
// makes wide diagrams illegible while narrower ones look comparatively
// larger. CSS alone can't override this (width:auto on a replaced
// element still defers to the width attribute's percentage), so this
// rewrites each diagram's width to its own natural size directly,
// keeping text at a consistent, legible scale across every diagram.
// Pairs with the .mermaid { overflow-x: auto } rule in extra.css, which
// lets a wide diagram scroll within its own box instead of dragging the
// page width along with it.
(function () {
  function fixSvg(svg) {
    if (svg.dataset.sizeFixed) return;
    var naturalWidth = svg.style.maxWidth;
    if (naturalWidth && naturalWidth !== "none") {
      svg.style.width = naturalWidth;
      svg.style.maxWidth = "none";
    }
    svg.dataset.sizeFixed = "1";
  }

  function scan() {
    document.querySelectorAll(".mermaid svg").forEach(fixSvg);
  }

  scan();
  new MutationObserver(scan).observe(document.body, {
    childList: true,
    subtree: true,
  });
})();
