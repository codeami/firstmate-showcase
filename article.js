/* Day/night for the kit article pages. Load it in the head, so the saved choice
   is set before the body is drawn. The choice is the same "theme" key nav.js
   keeps for the other pages; the kit reads it as data-mode. */
(function () {
  var root = document.documentElement;
  try {
    var t = localStorage.getItem("theme");
    if (t === "light" || t === "dark") root.setAttribute("data-mode", t);
  } catch (e) { /* storage blocked: follow the system */ }

  function mode() {
    var m = root.getAttribute("data-mode");
    if (m) return m;
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("theme");
    if (!btn) return;
    function label() {
      var dark = mode() === "dark";
      btn.textContent = dark ? "Day" : "Night";
      btn.setAttribute("aria-label", dark ? "Switch to day mode" : "Switch to night mode");
    }
    btn.addEventListener("click", function () {
      var next = mode() === "dark" ? "light" : "dark";
      root.setAttribute("data-mode", next);
      try { localStorage.setItem("theme", next); } catch (e) { /* storage blocked: lasts for this page only */ }
      label();
    });
    label();
  });
})();
