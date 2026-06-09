/**
 * Post-render normalization that maps namumark renderer output to
 * modern markdown rendering conventions.
 *
 * - heading anchor link (#)
 * - code block toolbar (language label + copy button)
 * - table first-row → thead
 * - iframe responsive wrapper
 * - callout (admonition) class detection from inline background color
 * - redirect link → markdown-style callout
 * - bare URL autolinking
 *
 * Idempotent: every transformed node is flagged with data-md-processed.
 */

const PROCESSED = "data-md-processed";

const SKIP_TAGS = new Set([
    "A",
    "CODE",
    "PRE",
    "SCRIPT",
    "STYLE",
    "KBD",
    "TEXTAREA",
    "BUTTON",
    "DETAILS",
    "SUMMARY",
]);

function isSkippedAncestor(node: Node): boolean {
    let el: Node | null = node.parentNode;
    while (el && el.nodeType === 1 && el !== document.body) {
        if (SKIP_TAGS.has((el as Element).tagName)) return true;
        el = el.parentNode;
    }
    return false;
}

function processHeadings(root: Element): void {
    const headings = root.querySelectorAll<HTMLHeadingElement>(
        "h1, h2, h3, h4, h5, h6",
    );
    headings.forEach((h) => {
        if (h.hasAttribute(PROCESSED)) return;
        const span = h.querySelector<HTMLElement>("span[id]");
        const anchorId = (span && span.id) || h.id;
        if (!anchorId) return;
        const a = document.createElement("a");
        a.className = "md-anchor";
        a.href = "#" + anchorId;
        a.setAttribute("aria-hidden", "true");
        a.tabIndex = -1;
        a.textContent = "#";
        h.insertBefore(a, h.firstChild);
        h.setAttribute(PROCESSED, "1");
    });
}

function legacyCopy(text: string, cb: () => void): void {
    try {
        const ta = document.createElement("textarea");
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
    } catch {
        /* noop */
    }
}

function processCodeBlocks(root: Element): void {
    const pres = root.querySelectorAll<HTMLPreElement>('pre[id="syntax"]');
    pres.forEach((pre) => {
        if (pre.hasAttribute(PROCESSED)) return;
        const parent = pre.parentElement;
        if (parent && parent.classList.contains("md-code-block")) {
            pre.setAttribute(PROCESSED, "1");
            return;
        }
        const code = pre.querySelector<HTMLElement>("code");
        let lang = "text";
        if (code && code.className) {
            const found = code.className
                .split(/\s+/)
                .find((c) => c && !c.startsWith("hljs"));
            if (found) lang = found;
        }
        const wrap = document.createElement("div");
        wrap.className = "md-code-block";

        const toolbar = document.createElement("div");
        toolbar.className = "md-code-toolbar";

        const langLabel = document.createElement("span");
        langLabel.className = "md-code-lang";
        langLabel.textContent = lang;

        const copyBtn = document.createElement("button");
        copyBtn.type = "button";
        copyBtn.className = "md-code-copy";
        copyBtn.textContent = "Copy";
        copyBtn.addEventListener("click", () => {
            const text = (code ?? pre).textContent ?? "";
            const afterCopy = () => {
                copyBtn.setAttribute("data-copied", "1");
                copyBtn.textContent = "Copied";
                setTimeout(() => {
                    copyBtn.removeAttribute("data-copied");
                    copyBtn.textContent = "Copy";
                }, 1800);
            };
            if (navigator.clipboard?.writeText) {
                navigator.clipboard.writeText(text).then(afterCopy, () => {
                    legacyCopy(text, afterCopy);
                });
            } else {
                legacyCopy(text, afterCopy);
            }
        });

        toolbar.appendChild(langLabel);
        toolbar.appendChild(copyBtn);

        pre.parentNode!.insertBefore(wrap, pre);
        wrap.appendChild(toolbar);
        wrap.appendChild(pre);
        pre.setAttribute(PROCESSED, "1");
    });
}

function processTables(root: Element): void {
    const tables = root.querySelectorAll<HTMLTableElement>("table");
    tables.forEach((t) => {
        if (t.hasAttribute(PROCESSED)) return;
        if (!t.querySelector("thead")) {
            const firstRow = t.querySelector("tr");
            if (firstRow) {
                const thead = document.createElement("thead");
                t.insertBefore(thead, t.firstChild);
                thead.appendChild(firstRow);
                firstRow.querySelectorAll("td").forEach((td) => {
                    const th = document.createElement("th");
                    for (let i = 0; i < td.attributes.length; i++) {
                        const attr = td.attributes[i]!;
                        th.setAttribute(attr.name, attr.value);
                    }
                    while (td.firstChild) th.appendChild(td.firstChild);
                    td.parentNode!.replaceChild(th, td);
                });
            }
        }
        t.classList.add("md-table");
        t.setAttribute(PROCESSED, "1");
    });
}

function processIframes(root: Element): void {
    const frames = root.querySelectorAll<HTMLIFrameElement>("iframe");
    frames.forEach((f) => {
        if (f.hasAttribute(PROCESSED)) return;
        const parent = f.parentElement;
        if (parent && parent.classList.contains("md-iframe-wrap")) {
            f.setAttribute(PROCESSED, "1");
            return;
        }
        const wrap = document.createElement("div");
        wrap.className = "md-iframe-wrap";
        f.parentNode!.insertBefore(wrap, f);
        wrap.appendChild(f);
        f.setAttribute(PROCESSED, "1");
    });
}

function processRedirects(root: Element): void {
    const links = root.querySelectorAll<HTMLAnchorElement>("a");
    links.forEach((a) => {
        if (a.hasAttribute(PROCESSED)) return;
        const txt = (a.textContent ?? "").trim();
        if (txt !== "(GO)") return;
        const href = a.getAttribute("href") ?? "";
        let label = "Redirect target";
        const m = href.match(/\/w_from\/([^#?]+)/);
        if (m) {
            try {
                label = decodeURIComponent(m[1]!);
            } catch {
                label = m[1]!;
            }
        }
        a.classList.add("md-redirect");
        a.textContent = "→ " + label;
        a.setAttribute(PROCESSED, "1");
    });
}

function parseRgb(input: string): [number, number, number] | null {
    const s = input.trim().toLowerCase();
    const hexMatch = s.match(/#([0-9a-f]{3,8})/i);
    if (hexMatch) {
        let h = hexMatch[1]!;
        if (h.length === 3)
            h = h
                .split("")
                .map((c) => c + c)
                .join("");
        if (h.length >= 6) {
            const n = parseInt(h.slice(0, 6), 16);
            if (!isNaN(n))
                return [(n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff];
        }
    }
    const rm = s.match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
    if (rm) return [+rm[1]!, +rm[2]!, +rm[3]!];
    const named: Record<string, [number, number, number]> = {
        red: [255, 0, 0],
        orange: [255, 165, 0],
        yellow: [255, 255, 0],
        green: [0, 128, 0],
        blue: [0, 0, 255],
    };
    if (named[s]) return named[s]!;
    return null;
}

function classifyCallout(bgStr: string): string | null {
    const rgb = parseRgb(bgStr);
    if (!rgb) return null;
    const [r, g, b] = rgb;
    const luma = 0.299 * r + 0.587 * g + 0.114 * b;
    if (luma < 80 || luma > 245) return null;
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    if (max - min < 25) return null;
    if (r > 200 && g < 170 && b < 170) return "danger";
    if (r > 220 && g > 200 && b < 180) return "warning";
    if (g >= r && g > 180 && b < 200) return "tip";
    if (b > 200 && r < 220) return "note";
    return null;
}

function processCallouts(root: Element): void {
    const divs = root.querySelectorAll<HTMLDivElement>("div[style]");
    divs.forEach((d) => {
        if (d.hasAttribute(PROCESSED)) return;
        const style = d.getAttribute("style") ?? "";
        const m = style.match(/background(?:-color)?\s*:\s*([^;]+)/i);
        if (!m) return;
        const kind = classifyCallout(m[1]!);
        if (!kind) return;
        d.classList.add("md-callout", "md-callout-" + kind);
        d.setAttribute(PROCESSED, "1");
    });
}

const AUTOLINK_RE = /\bhttps?:\/\/[^\s<>"'`]+[^\s<>"'`.,;:!?\)\]]/g;

function processAutolinks(root: Element): void {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
        acceptNode: (n: Node) => {
            if (isSkippedAncestor(n)) return NodeFilter.FILTER_REJECT;
            const v = n.nodeValue ?? "";
            if (!v.includes("http")) return NodeFilter.FILTER_REJECT;
            return NodeFilter.FILTER_ACCEPT;
        },
    });
    const nodes: Text[] = [];
    let n: Node | null;
    while ((n = walker.nextNode())) nodes.push(n as Text);
    nodes.forEach((node) => {
        const text = node.nodeValue ?? "";
        AUTOLINK_RE.lastIndex = 0;
        if (!AUTOLINK_RE.test(text)) return;
        AUTOLINK_RE.lastIndex = 0;
        const frag = document.createDocumentFragment();
        let last = 0;
        let m: RegExpExecArray | null;
        while ((m = AUTOLINK_RE.exec(text)) !== null) {
            if (m.index > last)
                frag.appendChild(
                    document.createTextNode(text.slice(last, m.index)),
                );
            const a = document.createElement("a");
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
        node.parentNode!.replaceChild(frag, node);
    });
}

export function markdownize(root: Element | null): void {
    if (!root) return;
    if (!root.children.length) return;
    try {
        processHeadings(root);
    } catch {
        /* noop */
    }
    try {
        processCodeBlocks(root);
    } catch {
        /* noop */
    }
    try {
        processTables(root);
    } catch {
        /* noop */
    }
    try {
        processIframes(root);
    } catch {
        /* noop */
    }
    try {
        processRedirects(root);
    } catch {
        /* noop */
    }
    try {
        processCallouts(root);
    } catch {
        /* noop */
    }
    try {
        processAutolinks(root);
    } catch {
        /* noop */
    }
}
