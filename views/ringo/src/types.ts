export type TopMenuItem = {
    href: string;
    label: string;
    topic: boolean;
};

export type AddedMenuItem = {
    label: string;
    href: string;
};

export type DocumentMeta = {
    title: string;
    subTitle: string;
    lastEdit: string;
    viewCount: string;
    lengthDoc: string;
};

export type UserState = {
    name: string;
    auth: string;
    login: boolean;
    alarmCount: string;
    path: string;
};

export type WikiState = {
    wikiName: string;
    licenseHtml: string;
};

export type SidebarMode = "default" | "override";

export type SidebarOverride = {
    mode: "override";
    html: string;
};

export type SidebarDefault = {
    mode: "default";
};

export type InitialState = {
    document: DocumentMeta;
    user: UserState;
    wiki: WikiState;
    menu: TopMenuItem[];
    addedMenu: AddedMenuItem[];
    bodyHtml: string;
    preBodyHtml: string;
    postBodyHtml: string;
    sidebar: SidebarDefault | SidebarOverride;
    labels: Record<string, string>;
};

export type LabelKey =
    | "list"
    | "recent_change"
    | "recent_discussion"
    | "vote_list"
    | "bbs_main"
    | "tool"
    | "random"
    | "other_tool"
    | "admin_tool"
    | "upload"
    | "skin_setting"
    | "user_tool"
    | "user_setting"
    | "alarm"
    | "watchlist"
    | "star_doc"
    | "logout"
    | "login"
    | "register"
    | "added_menu"
    | "search"
    | "edit"
    | "discussion"
    | "bbs"
    | "last_edit_time"
    | "page_view"
    | "length_doc";
