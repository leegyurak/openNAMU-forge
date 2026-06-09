import styles from "./Search.module.css";
import { Icon } from "../../lib/icons";

type Props = {
    placeholder: string;
};

export function Search({ placeholder }: Props) {
    return (
        <form className={styles.form} method="post" action="/search" role="search">
            <input
                className={styles.input}
                name="search"
                placeholder={placeholder}
                autoComplete="off"
                type="search"
            />
            <button type="submit" formAction="/goto" className={styles.button} aria-label="goto">
                <Icon name="ic:round-find-in-page" />
            </button>
            <button type="submit" formAction="/search" className={styles.button} aria-label="search">
                <Icon name="ic:baseline-search" />
            </button>
        </form>
    );
}
