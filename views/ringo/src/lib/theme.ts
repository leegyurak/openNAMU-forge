function readCookie(name: string): string | null {
    const pattern = new RegExp(`(?:^|; )${name}=([^;]*)`);
    const match = document.cookie.match(pattern);
    return match ? match[1] : null;
}

export function applyClientSkinSettings(): void {
    const useSystem =
        window.localStorage.getItem("main_css_use_sys_darkmode") !== "0";
    if (useSystem) {
        const prefersDark = window.matchMedia(
            "(prefers-color-scheme: dark)",
        ).matches;
        const darkCookie = readCookie("main_css_darkmode");
        if (prefersDark && darkCookie !== "1") {
            document.cookie = "main_css_darkmode=1; path=/";
            window.location.reload();
            return;
        }
        if (!prefersDark && darkCookie === "1") {
            document.cookie = "main_css_darkmode=0; path=/";
            window.location.reload();
            return;
        }
    }

    if (readCookie("main_css_darkmode") === "1") {
        document.documentElement.dataset.theme = "dark";
    } else {
        document.documentElement.dataset.theme = "light";
    }

    const fixedWidth = window.localStorage.getItem("main_css_fixed_width");
    if (fixedWidth && fixedWidth !== "") {
        const styleEl = document.getElementById("ringo_add_style");
        if (styleEl) {
            styleEl.textContent += `\n.ringo_section { max-width: ${fixedWidth}px !important; }`;
        }
    }
}
