/* tessera — charts.js
   ----------------------------------------------------------------------------
   Lazy rendering for the three optional renderers — Plotly, Mermaid, Tabulator.
   Each is a no-op if its library isn't bundled. Tables build the first time
   their slide is shown (so they measure while visible) and redraw on every
   (re)activation and on stage re-fit.

   T.state: none.   Calls: T.expandCell (expandPlotly delegates to it).
   Registers: T.initPlotlyCharts, T.resizePlotlyInSlide, T.renderMermaidInSlide,
              T.renderTabulatorsInSlide, T.expandPlotly.
   ------------------------------------------------------------------------- */
(function (T) {
  "use strict";

  // -- Plotly ----------------------------------------------
  // Pull text/grid colours from the active theme's CSS variables so Plotly
  // stays legible on light themes (where the old hardcoded light-grey font was
  // invisible). Axes inherit the font colour and a muted grid colour.
  function _plotlyThemeColors() {
    var cs = getComputedStyle(document.body);
    var text = (cs.getPropertyValue("--color-text") || "").trim() || "#eaeaea";
    var grid = (cs.getPropertyValue("--color-border") || "").trim() || "rgba(128,128,128,.3)";
    return { text: text, grid: grid };
  }

  function initPlotlyCharts() {
    if (typeof Plotly === "undefined") return;
    var c = _plotlyThemeColors();
    var axis = { gridcolor: c.grid, zerolinecolor: c.grid, linecolor: c.grid };
    var containers = document.querySelectorAll(".plotly-container");
    containers.forEach(function(el) {
      try {
        var raw = el.getAttribute("data-fig");
        if (!raw) return;
        var fig = JSON.parse(raw);
        var base = fig.layout || {};
        var layout = Object.assign({}, base, {
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor:  "rgba(0,0,0,0)",
          font: Object.assign({ color: c.text }, base.font || {}, { color: c.text }),
          xaxis: Object.assign({}, axis, base.xaxis || {}),
          yaxis: Object.assign({}, axis, base.yaxis || {}),
          margin: { t: 30, r: 10, b: 40, l: 50 },
          autosize: true,
        });
        Plotly.newPlot(el, fig.data || [], layout, { responsive: true });
      } catch(e) {
        el.textContent = "Error rendering chart: " + e.message;
      }
    });
  }

  function renderMermaidInSlide(slideEl) {
    if (typeof mermaid === "undefined") return;
    var unprocessed = Array.from(slideEl.querySelectorAll("pre.mermaid")).filter(function(el) {
      return !el.getAttribute("data-processed");
    });
    if (unprocessed.length > 0) {
      mermaid.run({ nodes: unprocessed });
    }
  }

  function resizePlotlyInSlide(slideEl) {
    if (typeof Plotly === "undefined") return;
    var containers = slideEl.querySelectorAll(".plotly-container");
    containers.forEach(function(el) {
      if (el._fullLayout) Plotly.relayout(el, { autosize: true });
    });
  }

  // -- Tabulator -------------------------------------------
  // Build each interactive table the first time its slide is shown (so it is
  // measured while visible, not inside a display:none slide), then redraw on
  // every (re)activation and on resize to track the fixed-size stage scale.

  var _tabulatorFormatsReady = false;
  function ensureTabulatorFormats() {
    if (_tabulatorFormatsReady || typeof Tabulator === "undefined") return;
    _tabulatorFormatsReady = true;
    Tabulator.extendModule("format", "formatters", {
      // Continuous row numbers across paginated pages.
      // getPosition(true) returns the row's 1-based index in the full filtered
      // set (post-filter, post-sort, before pagination slicing), so the counter
      // never resets when the reader flips to a new page.
      rownumGlobal: function(cell) {
        try {
          var pos = cell.getRow().getPosition(true);
          return pos !== false ? pos : "";
        } catch(e) { return ""; }
      }
    });
  }

  function buildTabulator(el) {
    if (el._tbBuilt || typeof Tabulator === "undefined") return;
    ensureTabulatorFormats();
    var cfgEl = document.getElementById(el.id + "-cfg");
    if (!cfgEl) return;
    el._tbBuilt = true;
    try {
      var table = new Tabulator(el, JSON.parse(cfgEl.textContent));
      el._tabulator = table;
      var card = el.closest(".cell");
      if (card) {
        card.querySelectorAll("[data-tab-download]").forEach(function(b) {
          b.addEventListener("click", function() {
            var f = b.getAttribute("data-tab-download");
            table.download(f, "data." + f);
          });
        });
      }
    } catch (e) {
      el.textContent = "Error rendering table: " + e.message;
    }
  }

  function renderTabulatorsInSlide(slideEl) {
    if (typeof Tabulator === "undefined") return;
    slideEl.querySelectorAll(".tessera-tabulator").forEach(function(el) {
      buildTabulator(el);
      var t = el._tabulator;
      // Defer the redraw so it runs after the stage transform / layout settles.
      if (t) requestAnimationFrame(function() { try { t.redraw(true); } catch (e) {} });
    });
  }

  function expandPlotly(btn) {
    T.expandCell(btn);
  }

  T.initPlotlyCharts        = initPlotlyCharts;
  T.resizePlotlyInSlide     = resizePlotlyInSlide;
  T.renderMermaidInSlide    = renderMermaidInSlide;
  T.renderTabulatorsInSlide = renderTabulatorsInSlide;
  T.expandPlotly            = expandPlotly;

})(window.Tessera = window.Tessera || {});
