from pathlib import Path


def test_route_패키지는_presentation_routes_안에_있다():
    assert not Path("route").exists()
    assert Path("opennamu_forge/presentation/routes/__init__.py").exists()
