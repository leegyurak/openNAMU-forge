import os
import zipfile
import urllib.request

from .tool.func import *

from .main_sys_restart import main_sys_restart_do
from opennamu_forge.infrastructure.logging import get_logger

logger = get_logger(__name__)

UPDATE_REPOSITORY = os.getenv("NAMU_UPDATE_REPOSITORY", "opennamu-forge/opennamu-forge")
UPDATE_GITHUB_URL = "https://github.com/" + UPDATE_REPOSITORY


async def main_sys_update(golang_process):
    with get_db_connect() as conn:
        if await acl_check('', 'owner_auth', '', '') == 1:
            return await re_error(conn, 3)

        if flask.request.method == 'POST':
            await acl_check(tool = 'owner_auth', memo = 'update')

            update_setting = get_other_setting_repository().get("update")
            up_data = update_setting if update_setting in ['stable', 'beta', 'dev', 'dont_use'] else 'stable'

            logger.info('Update')
            
            if golang_process.poll() is None:
                golang_process.terminate()
                try:
                    golang_process.wait(timeout = 5)
                except subprocess.TimeoutExpired:
                    golang_process.kill()
                    try:
                        golang_process.wait(timeout = 5)
                    except subprocess.TimeoutExpired:
                        logger.error('Golang process not terminated properly.')
            
            if platform.system() == 'Linux' or platform.system() == 'Darwin':
                ok = []
                ok += [os.system('git remote rm origin')]
                ok += [os.system('git remote add origin ' + UPDATE_GITHUB_URL + '.git')]
                ok += [os.system('git fetch --depth=1 origin ' + up_data)]
                ok += [os.system('git reset --hard origin/' + up_data)]
                for for_a in ok[1:]:
                    if for_a != 0:
                        break
                else:
                    linux_exe_chmod()

                    threading.Thread(target = main_sys_restart_do).start()
                    return flask.Response(await get_lang("warning_restart"), status = 200)
                
                logger.error('Error : update failed')
            elif platform.system() == 'Windows':
                os.system('rd /s /q route')

                urllib.request.urlretrieve(UPDATE_GITHUB_URL + '/archive/' + up_data + '.zip', 'update.zip')
                    
                zipfile.ZipFile('update.zip').extractall('')
                
                update_dir = UPDATE_REPOSITORY.split('/')[-1] + '-' + up_data
                ok = os.system('xcopy /y /s /r ' + update_dir + ' .')
                if ok == 0:
                    os.system('rd /s /q ' + update_dir)
                    os.system('del update.zip')
                    
                    threading.Thread(target = main_sys_restart_do).start()
                    return flask.Response(await get_lang("warning_restart"), status = 200)
            
            logger.error('Error : update failed')

            return await re_error(conn, 34)
        else:
            return await render_template(
                await get_lang('update'),
                await get_lang('update_warning') + '''
                    <hr class="main_hr">
                    <ul>
                        <li id="ver_send_2">''' + await get_lang('version') + ''' : </li>
                        <li id="ver_send">''' + await get_lang('lastest') + ''' : </li>
                    </ul>
                    <a href="''' + UPDATE_GITHUB_URL + '''">(Beta)</a> <a href="''' + UPDATE_GITHUB_URL + '''/tree/stable">(Stable)</a>
                    <hr class="main_hr">
                    <form method="post">
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('update') + '''</button>
                    </form>
                    <!-- JS : opennamu_forge_do_insert_version -->
                ''',
                0,
                [['manager', await get_lang('return')]]
            )
