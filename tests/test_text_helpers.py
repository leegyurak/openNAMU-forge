from opennamu_forge.presentation import text_helpers


def test_load_random_key는_요청한_길이의_문자열을_만든다():
    result = text_helpers.load_random_key(16)

    assert len(result) == 16
    assert result.isalnum()


def test_leng_check는_동일_길이면_0을_반환한다():
    assert text_helpers.leng_check(10, 10) == "0"


def test_leng_check는_감소분을_음수로_반환한다():
    assert text_helpers.leng_check(10, 4) == "-6"


def test_leng_check는_증가분을_양수로_반환한다():
    assert text_helpers.leng_check(4, 10) == "+6"


def test_number_check는_int_문자열을_그대로_반환한다():
    assert text_helpers.number_check("12") == "12"


def test_number_check는_float_모드에서_float_문자열을_그대로_반환한다():
    assert text_helpers.number_check("12.5", f=1) == "12.5"


def test_number_check는_숫자가_아니면_1을_반환한다():
    assert text_helpers.number_check("abc") == "1"


def test_get_tool_js_safe는_js_문자열_위험문자를_escape한다():
    assert text_helpers.get_tool_js_safe("a\nb\\c'd\"") == "a\\\\\\\\nb\\\\c\\'d\\\""


def test_cache_v는_기존_cache_suffix를_유지한다():
    assert text_helpers.cache_v() == ".cache_v289"


def test_cut_100은_기존_빈_문자열_동작을_유지한다():
    assert text_helpers.cut_100("anything") == ""
