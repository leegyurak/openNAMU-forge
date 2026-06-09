import { useCallback, useEffect, useRef, useState } from "react";
import styles from "./FloatingSidebar.module.css";
import { getLabel } from "../../lib/islands";

type Tab = 0 | 1 | 2;

type Props = {
    labels: Record<string, string>;
};

type CacheState = [string, string, string];

function xssEncode(input: string): string {
    return input
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#x27;");
}

async function fetchTab1(): Promise<string> {
    const res = await fetch("/api/recent_change/10");
    const data: Array<string[]> = await res.json();
    return data
        .filter((row) => row[6] === "")
        .map((row) => {
            const href = `/w/${encodeURIComponent(row[1])}`;
            return `<a href="${href}">${xssEncode(row[1])}</a><br>${row[2]} | ${xssEncode(row[3])}<br>`;
        })
        .join("");
}

async function fetchTab2(): Promise<string> {
    const res = await fetch("/api/recent_discuss/10");
    const data: Array<string[]> = await res.json();
    return data
        .map((row) => {
            const href = `/thread/${encodeURIComponent(row[3])}`;
            return `<a href="${href}">${xssEncode(row[1])}</a><br>${row[2]} | ${row[5]}<br>`;
        })
        .join("");
}

async function fetchTab3(): Promise<string> {
    const res = await fetch("/api/v2/bbs/main");
    const payload = await res.json();
    const data: Array<{
        set_id: string;
        set_code: string;
        title: string;
        date: string;
        user_id: string;
    }> = payload?.data ?? [];
    return data
        .map(
            (row) =>
                `<a href="/bbs/w/${row.set_id}/${row.set_code}">${xssEncode(row.title)}</a><br>${row.date} | ${row.user_id}<br>`,
        )
        .join("");
}

export function FloatingSidebar({ labels }: Props) {
    const [tab, setTab] = useState<Tab>(0);
    const [content, setContent] = useState<string>("Loading...");
    const cache = useRef<CacheState>(["", "", ""]);

    const loadTab = useCallback(async (next: Tab) => {
        const cached = cache.current[next];
        if (cached) {
            setContent(cached);
            return;
        }
        setContent("Loading...");
        try {
            const html =
                next === 0
                    ? await fetchTab1()
                    : next === 1
                      ? await fetchTab2()
                      : await fetchTab3();
            cache.current[next] = html || "";
            setContent(html || "");
        } catch {
            setContent("Error");
        }
    }, []);

    useEffect(() => {
        const offSidebar =
            window.localStorage.getItem("main_css_off_sidebar") === "0";
        if (offSidebar) {
            loadTab(0);
        }
    }, [loadTab]);

    const handleSelect = useCallback(
        (next: Tab) => {
            setTab(next);
            loadTab(next);
        },
        [loadTab],
    );

    return (
        <aside className={styles.root} aria-label="document side panel">
            <div className={styles.tabs} role="tablist">
                <button
                    type="button"
                    id="side_button_1"
                    role="tab"
                    aria-selected={tab === 0}
                    className={`${styles.tabButton} ${tab === 0 ? styles.tabButtonActive : ""}`}
                    onClick={() => handleSelect(0)}
                >
                    {getLabel(labels, "edit")}
                </button>
                <button
                    type="button"
                    id="side_button_2"
                    role="tab"
                    aria-selected={tab === 1}
                    className={`${styles.tabButton} ${tab === 1 ? styles.tabButtonActive : ""}`}
                    onClick={() => handleSelect(1)}
                >
                    {getLabel(labels, "discussion")}
                </button>
                <button
                    type="button"
                    id="side_button_3"
                    role="tab"
                    aria-selected={tab === 2}
                    className={`${styles.tabButton} ${tab === 2 ? styles.tabButtonActive : ""}`}
                    onClick={() => handleSelect(2)}
                >
                    {getLabel(labels, "bbs")}
                </button>
            </div>
            <div
                id="side_content"
                className={styles.content}
                dangerouslySetInnerHTML={{ __html: content }}
            />
        </aside>
    );
}

export function SidebarOverride({ html }: { html: string }) {
    return (
        <aside
            className={`${styles.root} ${styles.override}`}
            dangerouslySetInnerHTML={{ __html: html }}
        />
    );
}
