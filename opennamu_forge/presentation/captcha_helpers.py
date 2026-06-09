from __future__ import annotations

import flask

from opennamu_forge.application.dto.captcha import CaptchaVerificationRequest
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import (
    get_captcha_client,
    get_other_setting_repository,
)

VERIFY_URLS = {
    "": "https://www.google.com/recaptcha/api/siteverify",
    "v3": "https://www.google.com/recaptcha/api/siteverify",
    "cf": "https://challenges.cloudflare.com/turnstile/v0/siteverify",
    "h": "https://hcaptcha.com/siteverify",
}


async def captcha_get() -> str:
    data = ""

    if await _can_skip_captcha():
        return data

    if await acl_check("", "recaptcha") != 1:
        return data

    settings = get_other_setting_repository()
    recaptcha = settings.get("recaptcha")
    sec_re = settings.get("sec_re")
    rec_ver = settings.get("recaptcha_ver")
    if recaptcha == "" or sec_re == "":
        return data

    if rec_ver == "":
        data += (
            '<script defer src="https://www.google.com/recaptcha/api.js"></script>'
            + '<div class="g-recaptcha" data-sitekey="'
            + recaptcha
            + '"></div>'
            + '<hr class="main_hr">'
        )
    elif rec_ver == "v3":
        data += (
            '<script defer src="https://www.google.com/recaptcha/api.js?render='
            + recaptcha
            + '"></script>'
            + '<input class="__ON_INPUT__" type="hidden" id="g-recaptcha" name="g-recaptcha">'
            + '<script type="text/javascript">'
            + "document.addEventListener('DOMContentLoaded', function () {"
            + "grecaptcha.ready(function() {"
            + "grecaptcha.execute('"
            + recaptcha
            + "', {action: 'homepage'}).then(function(token) {"
            + "document.getElementById('g-recaptcha').value = token;"
            + "});"
            + "});"
            + "});"
            + "</script>"
        )
    elif rec_ver == "cf":
        data += (
            '<script defer src="https://challenges.cloudflare.com/turnstile/v0/api.js?compat=recaptcha"></script>'
            + '<div class="g-recaptcha" data-sitekey="'
            + recaptcha
            + '"></div>'
            + '<hr class="main_hr">'
        )
    else:
        data += (
            '<script defer src="https://js.hcaptcha.com/1/api.js"></script>'
            + '<div class="h-captcha" data-sitekey="'
            + recaptcha
            + '"></div>'
            + '<hr class="main_hr">'
        )

    return data


async def captcha_post(re_data: str) -> int:
    if await _can_skip_captcha():
        pass
    elif await acl_check("", "recaptcha") == 1:
        settings = get_other_setting_repository()
        sec_re = settings.get("sec_re")
        rec_ver = settings.get("recaptcha_ver")
        if await captcha_get() != "":
            verified = await get_captcha_client().verify(
                CaptchaVerificationRequest(
                    verify_url=VERIFY_URLS.get(rec_ver, VERIFY_URLS["h"]),
                    secret=sec_re,
                    response=re_data,
                )
            )
            if not verified:
                return 1

    _update_captcha_pass()

    return 0


async def _can_skip_captcha() -> bool:
    return (
        await acl_check("", "recaptcha_five_pass") == 0
        and "recapcha_pass" in flask.session
        and flask.session["recapcha_pass"] > 0
    )


def _update_captcha_pass() -> None:
    if "recapcha_pass" in flask.session:
        if flask.session["recapcha_pass"] > 0:
            flask.session["recapcha_pass"] -= 1
        else:
            flask.session["recapcha_pass"] = 5
    else:
        flask.session["recapcha_pass"] = 5
