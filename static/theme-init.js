(function () {
  var savedTheme = localStorage.getItem("theme");
  var systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  var theme = savedTheme || (systemPrefersDark ? "dark" : "light");
  document.documentElement.setAttribute("data-bs-theme", theme);
})();
