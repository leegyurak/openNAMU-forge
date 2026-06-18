import { useEffect, useRef } from "react";
import styles from "./DocumentView.module.css";
import { getLabel } from "../../lib/islands";
import { markdownize } from "../../lib/markdownize";
import type { DocumentMeta, TopMenuItem, WikiState } from "../../types";

type Props = {
    document: DocumentMeta;
    menu: TopMenuItem[];
    wiki: WikiState;
    preBodyHtml: string;
    bodyHtml: string;
    postBodyHtml: string;
    labels: Record<string, string>;
};

export function DocumentView({
    document,
    menu,
    wiki,
    preBodyHtml,
    bodyHtml,
    postBodyHtml,
    labels,
}: Props) {
    const showSubTitle = document.subTitle && document.subTitle !== "0";
    const showMeta = document.lastEdit && document.lastEdit !== "0";

    const bodyRef = useRef<HTMLDivElement | null>(null);
    useEffect(() => {
        markdownize(bodyRef.current);
    }, [preBodyHtml, bodyHtml, postBodyHtml]);

    return (
        <section className={styles.section}>
            <div className={styles.titleBlock}>
                <h1 className={styles.title}>
                    <span>{document.title}</span>
                    {showSubTitle && (
                        <sub className={styles.subTitle}>{document.subTitle}</sub>
                    )}
                </h1>
                {showMeta && (
                    <div className={styles.meta}>
                        <span className={styles.metaItem}>
                            {getLabel(labels, "last_edit_time")} : {document.lastEdit}
                        </span>
                        {document.viewCount && document.viewCount !== "0" && (
                            <span className={styles.metaItem}>
                                {getLabel(labels, "page_view")} : {document.viewCount}
                            </span>
                        )}
                        {document.lengthDoc && document.lengthDoc !== "" && (
                            <span className={styles.metaItem}>
                                {getLabel(labels, "length_doc")} : {document.lengthDoc}
                            </span>
                        )}
                    </div>
                )}
                {menu.length > 0 && (
                    <div className={styles.menu}>
                        {menu.map((item) => (
                            <a
                                key={item.href + item.label}
                                href={item.href}
                                className={`${styles.menuItem} ${item.topic ? styles.menuItemActive : ""}`}
                            >
                                {item.label}
                            </a>
                        ))}
                    </div>
                )}
            </div>
            <article className={styles.bodyShell} id="main_data">
                <div
                    ref={bodyRef}
                    className={`${styles.body} opennamu_forge_main`}
                    dangerouslySetInnerHTML={{
                        __html: preBodyHtml + bodyHtml + postBodyHtml,
                    }}
                />
            </article>
            <footer className={styles.footer} id="footer">
                <div dangerouslySetInnerHTML={{ __html: wiki.licenseHtml }} />
                <a
                    className={styles.footerLogo}
                    href="https://github.com/leegyurak/openNAMU-forge"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <img alt="opennamu-forge logo" src="/views/main_css/file/s_logo.webp" />
                </a>
            </footer>
        </section>
    );
}
