from __future__ import annotations

import hashlib

from opennamu_forge.presentation.dependencies import (
    get_other_setting_repository,
    get_user_setting_repository,
)


def pw_encode(data, db_data_encode=""):
    if db_data_encode == "":
        db_data_encode = get_other_setting_repository().get("encode", default="sha3")

    if db_data_encode == "sha256":
        return hashlib.sha256(bytes(data, "utf-8")).hexdigest()
    if db_data_encode == "sha3":
        return hashlib.sha3_256(bytes(data, "utf-8")).hexdigest()
    if db_data_encode == "sha3-512":
        return hashlib.sha3_512(bytes(data, "utf-8")).hexdigest()

    db_data_salt = get_other_setting_repository().get("salt_key")
    if db_data_encode == "sha3-salt":
        return hashlib.sha3_256(bytes(data + db_data_salt, "utf-8")).hexdigest()

    return hashlib.sha3_512(bytes(data + db_data_salt, "utf-8")).hexdigest()


def pw_check(data, data2, type_d="no", id_d=""):
    load_set_data = get_other_setting_repository().get("encode") or "sha3"

    set_data = load_set_data
    if type_d != "no":
        set_data = "sha3" if type_d == "" else type_d

    re_data = 1 if pw_encode(data, set_data) == data2 else 0
    if load_set_data != set_data and re_data == 1 and id_d != "":
        user_settings = get_user_setting_repository()
        user_settings.upsert(id_d, "pw", pw_encode(data))
        user_settings.upsert(id_d, "encode", load_set_data)

    return re_data
