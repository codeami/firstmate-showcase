/* Shared shell for every page: sidebar nav, header with day/night toggle,
   draft banner, byline and previous/next links. No build step, no network.
   To add or rename a page, edit one line in PAGES. Order here is reading order. */
var DRAFT = false; // false removes the draft banner on every page

var PAGES = [
  ["index.html",     "The story"],
  ["overview.html",  "The six lanes"],
  ["s02.html",       "Supervisor"],
  ["s03.html",       "Crews"],
  ["s04.html",       "Context system"],
  ["s05.html",       "Hooks and rules"],
  ["skills.html",    "How skills work"],
  ["s06.html",       "Memory and index"],
  ["s07.html",       "Review surfaces"],
  ["s08.html",       "Planning side"],
  ["cast.html",      "Cast and authority"],
  ["tasks.html",     "Task management"],
  ["testing.html",   "Testing in public"],
  ["vendors.html",   "Agents as vendors"],
  ["s09.html",       "What works today"],
  ["s10.html",       "Influences"],
  ["changelog.html", "Changelog"]
];

var SITE = "Six-Lane Agent Setup";

/* Theme: follow the system unless the reader picked one. The choice is kept in
   localStorage. This runs in the head, before the body is drawn, so there is
   no flash. */
function validTheme(t) { return t === "light" || t === "dark" ? t : null; }
function readTheme() {
  try { return validTheme(localStorage.getItem("theme")); } catch (e) { return null; }
}
function saveTheme(t) {
  try { localStorage.setItem("theme", t); } catch (e) { /* storage blocked: the choice lasts for this page only */ }
}
var chosenTheme = readTheme();
function currentTheme() {
  var set = document.documentElement.getAttribute("data-theme");
  if (set) return set;
  return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}
if (chosenTheme) {
  document.documentElement.setAttribute("data-theme", chosenTheme);
}

function meta(name) {
  var m = document.querySelector('meta[name="' + name + '"]');
  return m ? m.getAttribute("content") : "";
}

function el(tag, attrs, text) {
  var n = document.createElement(tag);
  for (var k in attrs) n.setAttribute(k, attrs[k]);
  if (text) n.textContent = text;
  return n;
}

function buildShell() {
  var here = location.pathname.split("/").pop() || "index.html";
  var idx = -1;
  for (var i = 0; i < PAGES.length; i++) if (PAGES[i][0] === here) idx = i;
  var main = document.querySelector("main");
  if (!main) return;

  var app = el("div", { "class": "app" });
  var side = el("aside", { "class": "side", id: "side" });
  var brand = el("a", { "class": "brand", href: "index.html" }, SITE);
  side.appendChild(brand);
  side.appendChild(el("div", { "class": "lbl side-sub" }, DRAFT ? "Private draft" : "Notes"));
  var nav = el("nav", { "aria-label": "Pages" });
  PAGES.forEach(function (p, n) {
    var a = el("a", { "class": "nav", href: p[0] }, p[1]);
    if (n === idx) a.setAttribute("aria-current", "page");
    nav.appendChild(a);
  });
  side.appendChild(nav);

  var col = el("div", { "class": "col" });
  var top = el("header", { "class": "top" });
  var menu = el("button", { "class": "menu", type: "button", "aria-controls": "side", "aria-expanded": "false" }, "Menu");
  menu.addEventListener("click", function () {
    var open = app.classList.toggle("nav-open");
    menu.setAttribute("aria-expanded", open ? "true" : "false");
  });
  var where = el("span", { "class": "lbl where" }, idx >= 0 ? PAGES[idx][1] : "");
  var toggle = el("button", { "class": "theme", type: "button" });
  function label() {
    var dark = currentTheme() === "dark";
    toggle.textContent = dark ? "Day" : "Night";
    toggle.setAttribute("aria-label", dark ? "Switch to day mode" : "Switch to night mode");
  }
  toggle.addEventListener("click", function () {
    var next = currentTheme() === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    chosenTheme = next;
    saveTheme(next);
    label();
  });
  label();
  top.appendChild(menu); top.appendChild(where); top.appendChild(toggle);
  col.appendChild(top);

  if (DRAFT) col.appendChild(el("div", { "class": "banner", role: "note" },
    "Private draft. Not published. Do not share."));

  main.parentNode.insertBefore(app, main);
  app.appendChild(side);
  app.appendChild(col);
  col.appendChild(main);

  var h1 = main.querySelector("h1");
  if (h1 && meta("date")) {
    var by = el("p", { "class": "byline lbl" },
      "Written " + meta("date") + (meta("last-updated") ? " · Updated " + meta("last-updated") : ""));
    h1.parentNode.insertBefore(by, h1.nextSibling);
  }

  if (idx >= 0) {
    var pager = el("nav", { "class": "pager", "aria-label": "Previous and next" });
    pager.appendChild(idx > 0 ? el("a", { href: PAGES[idx - 1][0], rel: "prev" }, "← " + PAGES[idx - 1][1]) : el("span"));
    pager.appendChild(idx < PAGES.length - 1 ? el("a", { href: PAGES[idx + 1][0], rel: "next" }, PAGES[idx + 1][1] + " →") : el("span"));
    main.appendChild(pager);
  }
}

/* In-page links: scroll with JS, with a smooth scroll and the same behaviour everywhere. */
function scrollToId(id) {
  var t = id && document.getElementById(id);
  if (!t) return false;
  t.scrollIntoView({ behavior: "smooth", block: "start" });
  try { history.replaceState(null, "", "#" + id); } catch (e) { /* sandbox may refuse */ }
  return true;
}
function samePageHash(a) {
  var href = a.getAttribute("href") || "";
  var i = href.indexOf("#");
  if (i < 0) return "";
  var page = href.slice(0, i).split("?")[0];
  var here = location.pathname.split("/").pop() || "index.html";
  return (page === "" || page === here) ? href.slice(i + 1) : "";
}
document.addEventListener("click", function (ev) {
  var a = ev.target.closest ? ev.target.closest("a[href]") : null;
  if (!a) return;
  var id = samePageHash(a);
  if (id && scrollToId(id)) ev.preventDefault();
});

function start() {
  buildShell();
  if (location.hash) scrollToId(decodeURIComponent(location.hash.slice(1)));
}
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
else start();
