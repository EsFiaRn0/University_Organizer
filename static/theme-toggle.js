(function () {
  var media = window.matchMedia("(prefers-color-scheme: dark)");
  var btn = document.getElementById("theme-toggle");
  var icon = btn ? btn.querySelector(".theme-icon") : null;
  if (!btn) return;

  function getTheme() {
    var saved = localStorage.getItem("theme");
    if (saved) return saved;
    return media.matches ? "dark" : "light";
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-bs-theme", theme);
    if (icon) {
      icon.innerHTML = theme === "dark"
        ? '<svg viewBox="0 0 24 24" role="presentation" focusable="false"><path d="M12 4.5a.75.75 0 0 1 .75.75v1.6a.75.75 0 0 1-1.5 0v-1.6a.75.75 0 0 1 .75-.75Zm0 12.05a.75.75 0 0 1 .75.75v1.7a.75.75 0 0 1-1.5 0v-1.7a.75.75 0 0 1 .75-.75ZM5.25 11.8a.75.75 0 0 1 .75.75v.05a.75.75 0 0 1-1.5 0v-.05a.75.75 0 0 1 .75-.75Zm12.75 0a.75.75 0 0 1 .75.75v.05a.75.75 0 0 1-1.5 0v-.05a.75.75 0 0 1 .75-.75ZM7.2 6.7a.75.75 0 0 1 1.06 0l1.1 1.1a.75.75 0 1 1-1.06 1.06L7.2 7.76a.75.75 0 0 1 0-1.06Zm8.44 8.43a.75.75 0 0 1 1.06 0l1.1 1.1a.75.75 0 1 1-1.06 1.06l-1.1-1.1a.75.75 0 0 1 0-1.06ZM16.7 6.7a.75.75 0 0 1 1.06 1.06l-1.1 1.1A.75.75 0 1 1 15.6 7.8l1.1-1.1ZM8.3 15.13a.75.75 0 0 1 1.06 1.06l-1.1 1.1a.75.75 0 0 1-1.06-1.06l1.1-1.1ZM12 8.2a4 4 0 1 1 0 8 4 4 0 0 1 0-8Z"/></svg>'
        : '<svg viewBox="0 0 24 24" role="presentation" focusable="false"><path d="M14.25 3.2a.75.75 0 0 1 .72.95 7.8 7.8 0 0 0-.35 2.3 7.95 7.95 0 0 0 7.95 7.95c.73 0 1.44-.1 2.11-.29a.75.75 0 0 1 .88.98 10.25 10.25 0 1 1-11.3-13.89ZM13.18 5a8.75 8.75 0 1 0 9.04 10.43c-.21.02-.43.03-.65.03A9.45 9.45 0 0 1 12.12 6c0-.34.02-.67.06-1Z"/></svg>';
    }
  }

  applyTheme(getTheme());

  btn.addEventListener("click", function () {
    var current = document.documentElement.getAttribute("data-bs-theme") || "light";
    var next = current === "dark" ? "light" : "dark";
    localStorage.setItem("theme", next);
    applyTheme(next);
  });

  media.addEventListener("change", function () {
    if (localStorage.getItem("theme")) return;
    applyTheme(media.matches ? "dark" : "light");
  });
})();
