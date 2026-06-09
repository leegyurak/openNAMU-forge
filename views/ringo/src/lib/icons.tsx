type IconProps = {
    name: string;
    inline?: boolean;
    "aria-hidden"?: boolean;
};

export function Icon({
    name,
    inline = true,
    "aria-hidden": ariaHidden = true,
}: IconProps) {
    return (
        <span
            className="iconify"
            data-icon={name}
            data-inline={inline ? "true" : "false"}
            aria-hidden={ariaHidden}
        />
    );
}
