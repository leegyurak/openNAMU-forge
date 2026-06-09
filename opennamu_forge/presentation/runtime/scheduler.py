from __future__ import annotations

import asyncio
import datetime
import os
import re
import shutil
import threading
from collections.abc import Mapping

from opennamu_forge.infrastructure.logging import get_logger
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import (
    get_admin_repository,
    get_document_meta_repository,
    get_other_setting_repository,
    get_recent_block_repository,
    get_user_agent_repository,
    get_user_setting_repository,
    get_vote_repository,
)
from opennamu_forge.presentation.shared.sql_dialect import get_time
from opennamu_forge.presentation.text_helpers import number_check

logger = get_logger(__name__)

_daily_task = None
_daily_thread = None

async def make_auto_sitemap() -> None:
    from opennamu_forge.presentation.routes.main_setting_sitemap import main_setting_sitemap

    await main_setting_sitemap(1)

def back_up(data_db_set: Mapping[str, str]) -> None:
    try:
        settings = get_other_setting_repository()
        back_time_data = settings.get("back_up")
        back_time = float(number_check(back_time_data, True)) if back_time_data != "" else 0

        back_up_count_data = settings.get("backup_count")
        back_up_count = int(number_check(back_up_count_data)) if back_up_count_data != "" else 3

        if back_time != 0:
            back_up_where = settings.get("backup_where") or data_db_set["name"] + ".db"

            logger.info("Back up state : %s hours", back_time)
            logger.info("Back up directory : %s", back_up_where)
            if back_up_count != 0:
                logger.info("Back up max number : %s", back_up_count)

                file_dir = os.path.split(back_up_where)[0]
                file_dir = "." if file_dir == "" else file_dir

                file_name = os.path.split(back_up_where)[1]
                file_name = re.sub(r"\.db$", "_[0-9]{14}.db", file_name)

                backup_file = [
                    backup_name for backup_name in os.listdir(file_dir) if re.search("^" + file_name + "$", backup_name)
                ]
                backup_file = sorted(backup_file)

                if len(backup_file) >= back_up_count:
                    remove_dir = os.path.join(file_dir, backup_file[0])
                    os.remove(remove_dir)
                    logger.info("Back up : Remove (%s)", remove_dir)

            now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_file_name = re.sub(r"\.db$", "_" + now_time + ".db", back_up_where)
            shutil.copyfile(data_db_set["name"] + ".db", new_file_name)

            logger.info("Back up : OK (%s)", new_file_name)
        else:
            logger.info("Back up state : Turn off")

            back_time = 1
    except Exception:
        logger.exception("Back up : Error")

        back_time = 1

    threading.Timer(60 * 60 * back_time, back_up, [data_db_set]).start()

async def do_every_day() -> None:
    time_today = get_time().split()[0]
    settings = get_other_setting_repository()
    votes = get_vote_repository()
    user_settings = get_user_setting_repository()
    document_meta = get_document_meta_repository()

    for vote in votes.list_by_types(("open", "n_open"), limit=100000):
        db_data = votes.get_option(vote.vote_id, "end_date")
        if db_data != "":
            time_db = db_data.split()[0]
            if time_today > time_db:
                votes.update_main_type(vote.vote_id, vote.type, "close" if vote.type == "open" else "n_close")

    get_recent_block_repository().close_expired(get_time())

    for auth_date in user_settings.list_id_data_by_name("auth_date"):
        time_db = auth_date[1].split()[0]
        if time_today > time_db:
            user_settings.upsert(auth_date[0], "acl", "user")
            user_settings.delete(auth_date[0], "auth_date")

    for acl_date in document_meta.list_doc_rev_data_by_set_name("acl_date"):
        time_db = acl_date[2].split()[0]
        if time_today > time_db:
            document_meta.delete_acl(acl_date[0], acl_date[1])
            document_meta.delete(acl_date[0], "acl_date", doc_rev=acl_date[1])

    db_data = settings.get("ua_expiration_date")
    if db_data != "":
        time_db = int(number_check(db_data))

        time_calc = datetime.date.today() - datetime.timedelta(days=time_db)
        time_calc = time_calc.strftime("%Y-%m-%d %H:%M:%S")

        get_user_agent_repository().delete_older_than(time_calc)

    db_data = settings.get("auth_history_expiration_date")
    if db_data != "":
        time_db = int(number_check(db_data))

        time_calc = datetime.date.today() - datetime.timedelta(days=time_db)
        time_calc = time_calc.strftime("%Y-%m-%d %H:%M:%S")

        get_admin_repository().delete_records_older_than(time_calc)

    db_data = settings.get("sitemap_auto_make")
    if db_data != "":
        await make_auto_sitemap()

        logger.info("Make sitemap")

    for user_id in user_settings.list_ids_by_name_data("user_title", "✅"):
        if await acl_check("", "all_admin_auth", "", user_id) == 1:
            user_settings.update_user_title_checkmark(user_id)

async def daily_loop() -> None:
    while True:
        await do_every_day()
        await asyncio.sleep(60 * 60 * 24)

def _run_bg_loop_forever() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(daily_loop())
    loop.run_forever()

def start_daily_scheduler() -> None:
    global _daily_task, _daily_thread

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        if _daily_thread is None or not _daily_thread.is_alive():
            _daily_thread = threading.Thread(target=_run_bg_loop_forever, daemon=True)
            _daily_thread.start()
    else:
        if _daily_task is None or _daily_task.done():
            _daily_task = loop.create_task(daily_loop())

def auto_do_something(data_db_set: Mapping[str, str]) -> None:
    if data_db_set["type"] == "sqlite":
        back_up(data_db_set)

    start_daily_scheduler()
