import { useCallback, useMemo, useState } from "react";
import { Header } from "./components/header/Header";
import { Drawer } from "./components/drawer/Drawer";
import { DocumentView } from "./components/document/DocumentView";
import { FloatingSidebar, SidebarOverride } from "./components/sidebar/FloatingSidebar";
import { QuickNav } from "./components/nav/QuickNav";
import type { InitialState } from "./types";

type Props = {
    initial: InitialState;
};

export function App({ initial }: Props) {
    const [drawerOpen, setDrawerOpen] = useState(false);
    const openDrawer = useCallback(() => setDrawerOpen(true), []);
    const closeDrawer = useCallback(() => setDrawerOpen(false), []);

    const sidebar = useMemo(() => {
        if (initial.sidebar.mode === "override") {
            return <SidebarOverride html={initial.sidebar.html} />;
        }
        return <FloatingSidebar labels={initial.labels} />;
    }, [initial.labels, initial.sidebar]);

    return (
        <>
            <Header
                wikiName={initial.wiki.wikiName}
                user={initial.user}
                labels={initial.labels}
                onMenu={openDrawer}
            />
            <Drawer
                open={drawerOpen}
                onClose={closeDrawer}
                wikiName={initial.wiki.wikiName}
                user={initial.user}
                addedMenu={initial.addedMenu}
                labels={initial.labels}
            />
            <DocumentView
                document={initial.document}
                menu={initial.menu}
                wiki={initial.wiki}
                preBodyHtml={initial.preBodyHtml}
                bodyHtml={initial.bodyHtml}
                postBodyHtml={initial.postBodyHtml}
                labels={initial.labels}
            />
            {sidebar}
            <QuickNav />
        </>
    );
}
