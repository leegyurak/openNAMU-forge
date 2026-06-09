/*
 * markdownize — post-render normalization for namumark output.
 * Standalone vanilla JS for the current dist (mirrors src/lib/markdownize.ts).
 *
 *  - heading anchor link (#)
 *  - code block toolbar (language label + copy button)
 *  - table first-row -> thead.md-table
 *  - iframe responsive wrap
 *  - callout class detection from inline background
 *  - "(GO)" redirect link -> markdown callout
 *  - bare URL autolinking
 *
 * Idempotent via data-md-processed flag.
 */
(function () {
    "use strict";

    var ROOT_SELECTOR = ".opennamu_forge_main";
    var PROCESSED = "data-md-processed";
    var SKIP_TAGS = {
        A: 1,
        CODE: 1,
        PRE: 1,
        SCRIPT: 1,
        STYLE: 1,
        KBD: 1,
        TEXTAREA: 1,
        BUTTON: 1,
        DETAILS: 1,
        SUMMARY: 1,
    };

    function isSkippedAncestor(node) {
        var el = node.parentNode;
        while (el && el.nodeType === 1 && el !== document.body) {
            if (SKIP_TAGS[el.tagName]) return true;
            el = el.parentNode;
        }
        return false;
    }

    function processHeadings(root) {
        var headings = root.querySelectorAll("h1, h2, h3, h4, h5, h6");
        for (var i = 0; i < headings.length; i++) {
            var h = headings[i];
            if (h.hasAttribute(PROCESSED)) continue;
            var span = h.querySelector("span[id]");
            var anchorId = (span && span.id) || h.id;
            if (!anchorId) continue;
            var a = document.createElement("a");
            a.className = "md-anchor";
            a.href = "#" + anchorId;
            a.setAttribute("aria-hidden", "true");
            a.tabIndex = -1;
            a.textContent = "#";
            h.insertBefore(a, h.firstChild);
            h.setAttribute(PROCESSED, "1");
        }
    }

    function legacyCopy(text, cb) {
        try {
            var ta = document.createElement("textarea");
            ta.value = text;
            ta.style.position = "fixed";
            ta.style.top = "-1000px";
            ta.style.opacity = "0";
            document.body.appendChild(ta);
            ta.focus();
            ta.select();
            document.execCommand("copy");
            document.body.removeChild(ta);
            cb();
        } catch (e) {}
    }

    function processCodeBlocks(root) {
        var pres = root.querySelectorAll('pre[id="syntax"]');
        for (var i = 0; i < pres.length; i++) {
            (function (pre) {
                if (pre.hasAttribute(PROCESSED)) return;
                var parent = pre.parentNode;
                if (
                    parent &&
                    parent.classList &&
                    parent.classList.contains("md-code-block")
                ) {
                    pre.setAttribute(PROCESSED, "1");
                    return;
                }
                var code = pre.querySelector("code");
                var lang = "text";
                if (code && code.className) {
                    var classes = code.className.split(/\s+/);
                    for (var j = 0; j < classes.length; j++) {
                        var c = classes[j];
                        if (!c || c.indexOf("hljs") === 0) continue;
                        lang = c;
                        break;
                    }
                }
                var wrap = document.createElement("div");
                wrap.className = "md-code-block";

                var toolbar = document.createElement("div");
                toolbar.className = "md-code-toolbar";

                var langLabel = document.createElement("span");
                langLabel.className = "md-code-lang";
                langLabel.textContent = lang;

                var copyBtn = document.createElement("button");
                copyBtn.type = "button";
                copyBtn.className = "md-code-copy";
                copyBtn.textContent = "Copy";
                copyBtn.addEventListener("click", function () {
                    var text = (code || pre).textContent || "";
                    var afterCopy = function () {
                        copyBtn.setAttribute("data-copied", "1");
                        copyBtn.textContent = "Copied";
                        setTimeout(function () {
                            copyBtn.removeAttribute("data-copied");
                            copyBtn.textContent = "Copy";
                        }, 1800);
                    };
                    if (
                        navigator.clipboard &&
                        navigator.clipboard.writeText
                    ) {
                        navigator.clipboard
                            .writeText(text)
                            .then(afterCopy, function () {
                                legacyCopy(text, afterCopy);
                            });
                    } else {
                        legacyCopy(text, afterCopy);
                    }
                });

                toolbar.appendChild(langLabel);
                toolbar.appendChild(copyBtn);

                pre.parentNode.insertBefore(wrap, pre);
                wrap.appendChild(toolbar);
                wrap.appendChild(pre);
                pre.setAttribute(PROCESSED, "1");
            })(pres[i]);
        }
    }

    function processTables(root) {
        var tables = root.querySelectorAll("table");
        for (var i = 0; i < tables.length; i++) {
            var t = tables[i];
            if (t.hasAttribute(PROCESSED)) continue;
            if (!t.querySelector("thead")) {
                var firstRow = t.querySelector("tr");
                if (firstRow) {
                    var thead = document.createElement("thead");
                    t.insertBefore(thead, t.firstChild);
                    thead.appendChild(firstRow);
                    var tds = firstRow.querySelectorAll("td");
                    for (var j = 0; j < tds.length; j++) {
                        var td = tds[j];
                        var th = document.createElement("th");
                        for (var k = 0; k < td.attributes.length; k++) {
                            var attr = td.attributes[k];
                            th.setAttribute(attr.name, attr.value);
                        }
                        while (td.firstChild) th.appendChild(td.firstChild);
                        td.parentNode.replaceChild(th, td);
                    }
                }
            }
            t.classList.add("md-table");
            t.setAttribute(PROCESSED, "1");
        }
    }

    function processIframes(root) {
        var frames = root.querySelectorAll("iframe");
        for (var i = 0; i < frames.length; i++) {
            var f = frames[i];
            if (f.hasAttribute(PROCESSED)) continue;
            var parent = f.parentNode;
            if (
                parent &&
                parent.classList &&
                parent.classList.contains("md-iframe-wrap")
            ) {
                f.setAttribute(PROCESSED, "1");
                continue;
            }
            var wrap = document.createElement("div");
            wrap.className = "md-iframe-wrap";
            f.parentNode.insertBefore(wrap, f);
            wrap.appendChild(f);
            f.setAttribute(PROCESSED, "1");
        }
    }

    function processRedirects(root) {
        var links = root.querySelectorAll("a");
        for (var i = 0; i < links.length; i++) {
            var a = links[i];
            if (a.hasAttribute(PROCESSED)) continue;
            var txt = (a.textContent || "").trim();
            if (txt !== "(GO)") continue;
            var href = a.getAttribute("href") || "";
            var label = "Redirect target";
            var m = href.match(/\/w_from\/([^#?]+)/);
            if (m) {
                try {
                    label = decodeURIComponent(m[1]);
                } catch (e) {
                    label = m[1];
                }
            }
            a.classList.add("md-redirect");
            a.textContent = "→ " + label;
            a.setAttribute(PROCESSED, "1");
        }
    }

    function parseRgb(input) {
        var s = ("" + input).trim().toLowerCase();
        var hm = s.match(/#([0-9a-f]{3,8})/i);
        if (hm) {
            var h = hm[1];
            if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
            if (h.length >= 6) {
                var n = parseInt(h.slice(0, 6), 16);
                if (!isNaN(n))
                    return [(n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff];
            }
        }
        var rm = s.match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
        if (rm) return [+rm[1], +rm[2], +rm[3]];
        var named = {
            red: [255, 0, 0],
            orange: [255, 165, 0],
            yellow: [255, 255, 0],
            green: [0, 128, 0],
            blue: [0, 0, 255],
        };
        if (named[s]) return named[s];
        return null;
    }

    function classifyCallout(bgStr) {
        var rgb = parseRgb(bgStr);
        if (!rgb) return null;
        var r = rgb[0],
            g = rgb[1],
            b = rgb[2];
        var luma = 0.299 * r + 0.587 * g + 0.114 * b;
        if (luma < 80 || luma > 245) return null;
        var max = Math.max(r, g, b);
        var min = Math.min(r, g, b);
        if (max - min < 25) return null;
        if (r > 200 && g < 170 && b < 170) return "danger";
        if (r > 220 && g > 200 && b < 180) return "warning";
        if (g >= r && g > 180 && b < 200) return "tip";
        if (b > 200 && r < 220) return "note";
        return null;
    }

    function processCallouts(root) {
        var divs = root.querySelectorAll("div[style]");
        for (var i = 0; i < divs.length; i++) {
            var d = divs[i];
            if (d.hasAttribute(PROCESSED)) continue;
            var style = d.getAttribute("style") || "";
            var m = style.match(/background(?:-color)?\s*:\s*([^;]+)/i);
            if (!m) continue;
            var kind = classifyCallout(m[1]);
            if (!kind) continue;
            d.classList.add("md-callout");
            d.classList.add("md-callout-" + kind);
            d.setAttribute(PROCESSED, "1");
        }
    }

    var AUTOLINK_RE = /\bhttps?:\/\/[^\s<>"'`]+[^\s<>"'`.,;:!?\)\]]/g;
    function processAutolinks(root) {
        var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
            acceptNode: function (n) {
                if (isSkippedAncestor(n)) return NodeFilter.FILTER_REJECT;
                var v = n.nodeValue || "";
                if (v.indexOf("http") === -1) return NodeFilter.FILTER_REJECT;
                return NodeFilter.FILTER_ACCEPT;
            },
        });
        var nodes = [];
        var n;
        while ((n = walker.nextNode())) nodes.push(n);
        for (var i = 0; i < nodes.length; i++) {
            var node = nodes[i];
            var text = node.nodeValue || "";
            AUTOLINK_RE.lastIndex = 0;
            if (!AUTOLINK_RE.test(text)) continue;
            AUTOLINK_RE.lastIndex = 0;
            var frag = document.createDocumentFragment();
            var last = 0;
            var m;
            while ((m = AUTOLINK_RE.exec(text)) !== null) {
                if (m.index > last)
                    frag.appendChild(
                        document.createTextNode(text.slice(last, m.index)),
                    );
                var a = document.createElement("a");
                a.className = "md-autolink opennamu_forge_link_out";
                a.href = m[0];
                a.target = "_blank";
                a.rel = "noopener noreferrer";
                a.textContent = m[0];
                frag.appendChild(a);
                last = m.index + m[0].length;
            }
            if (last < text.length)
                frag.appendChild(document.createTextNode(text.slice(last)));
            node.parentNode.replaceChild(frag, node);
        }
    }

    function run() {
        var root = document.querySelector(ROOT_SELECTOR);
        if (!root) return false;
        if (!root.children || root.children.length === 0) return false;
        try {
            processHeadings(root);
        } catch (e) {}
        try {
            processCodeBlocks(root);
        } catch (e) {}
        try {
            processTables(root);
        } catch (e) {}
        try {
            processIframes(root);
        } catch (e) {}
        try {
            processRedirects(root);
        } catch (e) {}
        try {
            processCallouts(root);
        } catch (e) {}
        try {
            processAutolinks(root);
        } catch (e) {}
        return true;
    }

    function init() {
        if (run()) return;
        var attempts = 0;
        var interval = setInterval(function () {
            attempts++;
            if (run() || attempts > 40) clearInterval(interval);
        }, 60);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
