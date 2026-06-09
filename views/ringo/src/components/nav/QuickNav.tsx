import styles from "./QuickNav.module.css";
import { Icon } from "../../lib/icons";

export function QuickNav() {
    return (
        <nav className={styles.root} id="nav_bar" aria-label="quick navigation">
            <a className={styles.button} href="#main" id="go_top" aria-label="go top">
                <Icon name="ic:baseline-arrow-upward" />
            </a>
            <a className={styles.button} href="#footer" id="go_bottom" aria-label="go bottom">
                <Icon name="ic:baseline-arrow-downward" />
            </a>
            <a className={styles.button} href="#toc" id="go_toc" aria-label="go toc">
                <Icon name="ic:baseline-list" />
            </a>
        </nav>
    );
}
