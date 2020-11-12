from skam.app import app
from skam.server.server import subs, error_page

def test_can_render_skam_subs():
    with app.test_request_context():
        subs_page = subs("skam", 1, 1)
        assert subs_page != error_page()
