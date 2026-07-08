// Returns the platform-appropriate keyboard shortcut label for the search action.
// Displays "⌘K" on macOS and "Ctrl+K" on all other platforms.
function getSearchShortcut() {
  if (
    navigator.platform &&
    navigator.platform.toLowerCase().indexOf("mac") !== -1
  ) {
    return "⌘K";
  }

  return "Ctrl+K";
}

// Updates the search input's placeholder text and title attribute to show
// the platform-appropriate keyboard shortcut (e.g. "Search (⌘K)").
function updateSearchPlaceholder() {
  var searchQuery = document.querySelector(
    "[data-md-component='search-query']",
  );
  var shortcut = getSearchShortcut();

  if (!searchQuery) {
    return;
  }

  searchQuery.placeholder = "Search (" + shortcut + ")";
  searchQuery.title = "Search (" + shortcut + ")";
}

// Update the placeholder on initial page load and on MkDocs instant navigation page switches.
document.addEventListener("DOMContentLoaded", updateSearchPlaceholder);
document.addEventListener("DOMContentSwitch", updateSearchPlaceholder);

// Intercepts Cmd+K (macOS) / Ctrl+K (other platforms) to open the MkDocs search
// overlay and move focus to the search input.
document.addEventListener("keydown", function (event) {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    var searchToggle = document.getElementById("__search");
    var searchQuery = document.querySelector(
      "[data-md-component='search-query']",
    );

    if (!searchToggle || !searchQuery) {
      return;
    }

    event.preventDefault();
    searchToggle.checked = true;
    searchToggle.dispatchEvent(new Event("change"));

    window.setTimeout(function () {
      searchQuery.focus();
      searchQuery.select();
    }, 0);
  }
});
