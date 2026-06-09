import styles from "./Header.module.css";
import { Search } from "./Search";
import { Icon } from "../../lib/icons";
import { getLabel } from "../../lib/islands";
import type { UserState } from "../../types";

type Props = {
    wikiName: string;
    user: UserState;
    labels: Record<string, string>;
    onMenu: () => void;
};

export function Header({ wikiName, user, labels, onMenu }: Props) {
    const hasAlarm = user.login && user.alarmCount && user.alarmCount !== "0";
    const userHref = user.login ? "/user" : "/login";

    return (
        <header className={styles.root} id="main">
            <div className={styles.inner}>
                <button
                    type="button"
                    className={styles.hamburger}
                    onClick={onMenu}
                    aria-label="open navigation"
                >
                    <Icon name="ic:baseline-menu" />
                </button>
                <a className={styles.logo} href="/">
                    {wikiName || "openNAMU Forge"}
                </a>
                <div className={styles.searchSlot}>
                    <Search placeholder={getLabel(labels, "search")} />
                </div>
                <div className={styles.right}>
                    <a
                        href="/random"
                        className={styles.iconButton}
                        aria-label={getLabel(labels, "random")}
                        title={getLabel(labels, "random")}
                    >
                        <Icon name="ic:baseline-shuffle" />
                    </a>
                    <a
                        href="/recent_changes"
                        className={styles.iconButton}
                        aria-label={getLabel(labels, "recent_change")}
                        title={getLabel(labels, "recent_change")}
                    >
                        <Icon name="ic:baseline-access-time" />
                    </a>
                    <a
                        href={userHref}
                        className={`${styles.iconButton} ${hasAlarm ? styles.alarmDot : ""}`}
                        aria-label={user.login ? user.name : getLabel(labels, "login")}
                        title={user.login ? user.name : getLabel(labels, "login")}
                    >
                        <Icon
                            name={
                                user.login
                                    ? "ic:baseline-account-circle"
                                    : "ic:round-person-search"
                            }
                        />
                    </a>
                </div>
            </div>
            <div className={styles.mobileSearchBar}>
                <Search placeholder={getLabel(labels, "search")} />
            </div>
        </header>
    );
}
