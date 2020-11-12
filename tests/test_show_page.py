from skam.server.server import app, root, error_page


def test_can_load_sequential_page():
    with app.test_request_context():
        page = root("skam")
        assert page != error_page()


def test_can_load_standard_page():
    with app.test_request_context():
        page = root("nytt-paa-nytt")
        assert page != error_page()