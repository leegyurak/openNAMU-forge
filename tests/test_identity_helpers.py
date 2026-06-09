import asyncio

from opennamu_forge.presentation import identity_helpers


def test_ip_pas는_단일_ip를_변환한다(monkeypatch):
    calls = []

    async def fake_python_to_golang(func_name, other_set):
        calls.append((func_name, other_set))
        return {"data": {"127.0.0.1": "user"}}

    monkeypatch.setattr(identity_helpers, "python_to_golang", fake_python_to_golang)

    result = asyncio.run(identity_helpers.ip_pas("127.0.0.1"))

    assert result == "user"
    assert calls == [("api_func_ip_post", {"data_1": "127.0.0.1"})]


def test_ip_pas는_복수_ip를_변환한다(monkeypatch):
    calls = []

    async def fake_python_to_golang(func_name, other_set):
        calls.append((func_name, other_set))
        return {"data": {"127.0.0.1": "user", "192.0.2.1": "ip"}}

    monkeypatch.setattr(identity_helpers, "python_to_golang", fake_python_to_golang)

    result = asyncio.run(identity_helpers.ip_pas(["127.0.0.1", "192.0.2.1"]))

    assert result == {"127.0.0.1": "user", "192.0.2.1": "ip"}
    assert calls == [("api_func_ip_post", {"data_1": "127.0.0.1", "data_2": "192.0.2.1"})]
