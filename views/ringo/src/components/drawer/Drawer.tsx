import { useEffect } from "react";
import styles from "./Drawer.module.css";
import { Icon } from "../../lib/icons";
import { getLabel } from "../../lib/islands";
import type { AddedMenuItem, UserState } from "../../types";

export type DrawerLink = {
    href: string;
    icon: string;
    label: string;
    badge?: string;
};

export type DrawerSection = {
    title?: string;
    items: DrawerLink[];
};

type Props = {
    open: boolean;
    onClose: () => void;
    wikiName: string;
    user: UserState;
    addedMenu: AddedMenuItem[];
    labels: Record<string, string>;
};

function firstInitial(name: string): string {
    const trimmed = (name || "").trim();
    if (!trimmed) {
        return "?";
    }
    return trimmed.charAt(0).toUpperCase();
}

function buildSections(
    user: UserState,
    addedMenu: AddedMenuItem[],
    labels: Record<string, string>,
): DrawerSection[] {
    const recentSection: DrawerSection = {
        title: getLabel(labels, "list"),
        items: [
            {
                href: "/recent_changes",
                icon: "ic:baseline-autorenew",
                label: getLabel(labels, "recent_change"),
            },
            {
                href: "/recent_discuss",
                icon: "ic:baseline-add-comment",
                label: getLabel(labels, "recent_discussion"),
            },
            {
                href: "/vote",
                icon: "ic:baseline-how-to-vote",
                label: getLabel(labels, "vote_list"),
            },
            {
                href: "/bbs/main",
                icon: "ic:outline-developer-board",
                label: getLabel(labels, "bbs_main"),
            },
        ],
    };

    const toolItems: DrawerLink[] = [
        {
            href: "/random",
            icon: "ic:baseline-shuffle",
            label: getLabel(labels, "random"),
        },
        {
            href: "/other",
            icon: "ic:baseline-build",
            label: getLabel(labels, "other_tool"),
        },
        {
            href: "/upload",
            icon: "ic:baseline-cloud-upload",
            label: getLabel(labels, "upload"),
        },
        {
            href: "/change/skin_set",
            icon: "ic:baseline-settings",
            label: getLabel(labels, "skin_setting"),
        },
    ];
    if (user.auth !== "0") {
        toolItems.splice(2, 0, {
            href: "/manager",
            icon: "ic:baseline-how-to-reg",
            label: getLabel(labels, "admin_tool"),
        });
    }
    const toolSection: DrawerSection = {
        title: getLabel(labels, "tool"),
        items: toolItems,
    };

    const accountItems: DrawerLink[] = [
        {
            href: "/user",
            icon: "ic:baseline-account-box",
            label: getLabel(labels, "user_tool"),
        },
        {
            href: "/change",
            icon: "ic:baseline-manage-accounts",
            label: getLabel(labels, "user_setting"),
        },
    ];
    if (user.login) {
        accountItems.push(
            {
                href: "/alarm",
                icon: "ic:baseline-contact-mail",
                label: getLabel(labels, "alarm"),
                badge:
                    user.alarmCount && user.alarmCount !== "0"
                        ? user.alarmCount
                        : undefined,
            },
            {
                href: "/watch_list",
                icon: "ic:round-preview",
                label: getLabel(labels, "watchlist"),
            },
            {
                href: "/star_doc",
                icon: "ic:twotone-stars",
                label: getLabel(labels, "star_doc"),
            },
        );
    }
    const accountSection: DrawerSection = {
        title: user.login ? user.name : getLabel(labels, "user_tool"),
        items: accountItems,
    };

    const sections = [recentSection, toolSection, accountSection];

    if (addedMenu.length > 0) {
        sections.push({
            title: getLabel(labels, "added_menu"),
            items: addedMenu.map((item) => ({
                href: item.href,
                icon: "ic:baseline-plus",
                label: item.label,
            })),
        });
    }

    return sections;
}

export function Drawer({
    open,
    onClose,
    wikiName,
    user,
    addedMenu,
    labels,
}: Props) {
    useEffect(() => {
        if (open) {
            document.body.classList.add("drawer-open");
        } else {
            document.body.classList.remove("drawer-open");
        }
        return () => {
            document.body.classList.remove("drawer-open");
        };
    }, [open]);

    useEffect(() => {
        if (!open) {
            return;
        }
        const handleKey = (event: KeyboardEvent) => {
            if (event.key === "Escape") {
                onClose();
            }
        };
        document.addEventListener("keydown", handleKey);
        return () => document.removeEventListener("keydown", handleKey);
    }, [open, onClose]);

    const sections = buildSections(user, addedMenu, labels);

    const returnPath = user.path || "/";
    const hasAlarm = user.login && user.alarmCount && user.alarmCount !== "0";
    const subText = user.login
        ? hasAlarm
            ? `${getLabel(labels, "alarm")} ${user.alarmCount}`
            : ""
        : "";

    return (
        <>
            <div
                className={`${styles.backdrop} ${open ? styles.backdropOpen : ""}`}
                onClick={onClose}
                aria-hidden="true"
            />
            <aside
                className={`${styles.panel} ${open ? styles.panelOpen : ""}`}
                role="dialog"
                aria-modal="true"
                aria-label="navigation"
                aria-hidden={!open}
            >
                <div className={styles.head}>
                    <span className={styles.headTitle}>
                        {wikiName || "openNAMU Forge"}
                    </span>
                    <button
                        type="button"
                        className={styles.close}
                        onClick={onClose}
                        aria-label="close navigation"
                    >
                        <Icon name="ic:baseline-close" />
                    </button>
                </div>

                <div className={styles.userCard}>
                    <div className={styles.userTop}>
                        <span className={styles.avatar} aria-hidden="true">
                            {firstInitial(user.name)}
                        </span>
                        <div className={styles.userMeta}>
                            <div className={styles.userName}>
                                {user.login
                                    ? user.name
                                    : getLabel(labels, "login")}
                            </div>
                            {subText && (
                                <div className={styles.userSub}>{subText}</div>
                            )}
                        </div>
                    </div>
                    <div className={styles.userActions}>
                        {user.login ? (
                            <a
                                className={styles.userAction}
                                href={`/logout?return=${encodeURIComponent(returnPath)}`}
                            >
                                <Icon name="ic:baseline-logout" />
                                {getLabel(labels, "logout")}
                            </a>
                        ) : (
                            <>
                                <a
                                    className={styles.userAction}
                                    href={`/login?return=${encodeURIComponent(returnPath)}`}
                                >
                                    <Icon name="ic:baseline-login" />
                                    {getLabel(labels, "login")}
                                </a>
                                <a
                                    className={styles.userAction}
                                    href="/register"
                                >
                                    <Icon name="ic:baseline-person-add-alt-1" />
                                    {getLabel(labels, "register")}
                                </a>
                            </>
                        )}
                    </div>
                </div>

                <div className={styles.scroll}>
                    {sections.map((section, idx) => (
                        <div key={section.title ?? idx} className={styles.section}>
                            {section.title && (
                                <div className={styles.sectionTitle}>
                                    {section.title}
                                </div>
                            )}
                            {section.items.map((item) => (
                                <a
                                    key={item.href + item.label}
                                    href={item.href}
                                    className={styles.item}
                                    onClick={onClose}
                                >
                                    <Icon name={item.icon} />
                                    <span>{item.label}</span>
                                    {item.badge && (
                                        <span className={styles.itemBadge}>
                                            {item.badge}
                                        </span>
                                    )}
                                </a>
                            ))}
                        </div>
                    ))}
                </div>
            </aside>
        </>
    );
}
