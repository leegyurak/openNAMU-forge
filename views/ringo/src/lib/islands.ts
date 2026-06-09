import type {
    AddedMenuItem,
    InitialState,
    LabelKey,
    TopMenuItem,
} from "../types";

function readMeta(name: string): string {
    const el = document.querySelector<HTMLMetaElement>(
        `meta[name="ringo-app:${name}"]`,
    );
    return el?.content ?? "";
}

function readMetaFlag(name: string): boolean {
    return readMeta(name) === "1";
}

function readIslandHtml(id: string): string {
    const el = document.getElementById(`ringo-app-island-${id}`);
    return el?.innerHTML ?? "";
}

function readIslandText(id: string): string {
    const el = document.getElementById(`ringo-app-island-${id}`);
    return el?.textContent?.trim() ?? "";
}

function readTopMenu(): TopMenuItem[] {
    const root = document.getElementById("ringo-app-island-document-menu");
    if (!root) {
        return [];
    }
    const items = root.querySelectorAll<HTMLAnchorElement>("a[data-href]");
    const result: TopMenuItem[] = [];
    items.forEach((node) => {
        result.push({
            href: node.dataset.href ?? "",
            label: node.textContent?.trim() ?? "",
            topic: node.dataset.topic === "1",
        });
    });
    return result;
}

function readAddedMenu(): AddedMenuItem[] {
    const root = document.getElementById("ringo-app-island-added-menu");
    if (!root) {
        return [];
    }
    const items = root.querySelectorAll<HTMLAnchorElement>("a[data-href]");
    const result: AddedMenuItem[] = [];
    items.forEach((node) => {
        result.push({
            href: node.dataset.href ?? "",
            label: node.textContent?.trim() ?? "",
        });
    });
    return result;
}

function readLabels(): Record<string, string> {
    const root = document.getElementById("ringo-app-island-labels");
    if (!root) {
        return {};
    }
    const items = root.querySelectorAll<HTMLElement>("[data-key]");
    const result: Record<string, string> = {};
    items.forEach((node) => {
        const key = node.dataset.key;
        if (!key) {
            return;
        }
        result[key] = node.textContent ?? "";
    });
    return result;
}

export function loadInitialState(): InitialState {
    const sidebarOverrideHtml = readIslandHtml("sidebar-override");
    const hasOverride =
        document.getElementById("ringo-app-island-sidebar-override")?.dataset
            .empty === "0";

    return {
        document: {
            title: readMeta("doc-title"),
            subTitle: readMeta("doc-sub-title"),
            lastEdit: readMeta("doc-last-edit"),
            viewCount: readMeta("doc-view-count"),
            lengthDoc: readMeta("doc-length"),
        },
        user: {
            name: readMeta("user-name"),
            auth: readMeta("user-auth"),
            login: readMetaFlag("user-login"),
            alarmCount: readMeta("user-alarm-count"),
            path: readMeta("user-path"),
        },
        wiki: {
            wikiName: readMeta("wiki-name"),
            licenseHtml: readIslandHtml("license"),
        },
        menu: readTopMenu(),
        addedMenu: readAddedMenu(),
        bodyHtml: readIslandHtml("body"),
        preBodyHtml: readIslandHtml("pre-body"),
        postBodyHtml: readIslandHtml("post-body"),
        sidebar: hasOverride
            ? { mode: "override", html: sidebarOverrideHtml }
            : { mode: "default" },
        labels: readLabels(),
    };
}

export function getLabel(
    labels: Record<string, string>,
    key: LabelKey,
    fallback?: string,
): string {
    const value = labels[key];
    if (value && value.trim() !== "") {
        return value;
    }
    return fallback ?? key;
}

export { readIslandText };
