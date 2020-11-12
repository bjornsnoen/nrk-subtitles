from skam.server.server import app, index, error_page


def test_can_load_front_page():
    with app.test_request_context():
        contents = index()
        assert contents != error_page()
