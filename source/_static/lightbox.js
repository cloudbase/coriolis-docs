(function () {
  var skip =
    ".platform, .platform-vendors, .partner-logos, .video-preview, .video-previews, table.docutils";

  function eligible(img) {
    return img.closest(".rst-content") && !img.closest(skip) && !img.closest("a");
  }

  function init() {
    var images = document.querySelectorAll(".rst-content img");
    var targets = [];
    images.forEach(function (img) {
      if (eligible(img)) {
        targets.push(img);
      }
    });
    if (!targets.length) {
      return;
    }

    var overlay = document.createElement("div");
    overlay.className = "image-lightbox";
    overlay.hidden = true;
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Enlarged image");

    var enlarged = document.createElement("img");
    enlarged.alt = "";
    overlay.appendChild(enlarged);
    document.body.appendChild(overlay);

    var lastFocus = null;

    function open(img) {
      lastFocus = document.activeElement;
      enlarged.src = img.currentSrc || img.src;
      enlarged.alt = img.alt || "";
      overlay.hidden = false;
      document.body.classList.add("image-lightbox-open");
      overlay.focus();
    }

    function close() {
      overlay.hidden = true;
      enlarged.removeAttribute("src");
      enlarged.alt = "";
      document.body.classList.remove("image-lightbox-open");
      if (lastFocus && lastFocus.focus) {
        lastFocus.focus();
      }
    }

    overlay.tabIndex = -1;
    overlay.addEventListener("click", close);
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !overlay.hidden) {
        close();
      }
    });

    targets.forEach(function (img) {
      img.classList.add("lightbox-enabled");
      img.tabIndex = 0;
      img.setAttribute("role", "button");
      img.setAttribute("aria-haspopup", "dialog");
      img.addEventListener("click", function () {
        open(img);
      });
      img.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          open(img);
        }
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
