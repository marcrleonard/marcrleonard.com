// Cross-document view transitions. Loaded in <head> so the pagereveal listener
// is registered before first render. Tags the transition "back" when we are
// returning to a page higher up (concept -> index) or traversing history
// backwards, so the CSS can play the stack in reverse.
(function () {
  const rank = (url) => {
    const p = new URL(url, location.href).pathname.split("/").pop() || "index.html";
    return { "index.html": 0, "stack.html": 1, "deck.html": 2, "grid.html": 3 }[p] ?? 1;
  };
  addEventListener("pagereveal", (e) => {
    if (!e.viewTransition) return;
    const act = window.navigation && navigation.activation;
    const from = act && act.from && act.from.url;
    if (!from) return;
    e.viewTransition.types.add(rank(from) > rank(location.href) ? "back" : "forward");
  });
})();
