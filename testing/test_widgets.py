from unittest import main, TestCase
from unittest.mock import Mock, patch

from . import widgets


class Test_get_widgets(TestCase):
    def setUp(self):
        # This function is run before every test.

        # Replace `db` with a `Mock` instance in `widgets.py`.
        db_patcher = patch("testing.widgets.db")

        self.db = db_patcher.start()

        # Stop patching after each test. We don't want carryover between tests.
        self.addCleanup(db_patcher.stop)

    def test_db_is_properly_called(self):
        ids = [1, 2]
        widgets.get_widgets(ids)
        self.db.get_widgets.assert_called_with(ids)


class Test_save_widget(TestCase):
    def setUp(self):
        db_patcher = patch("testing.widgets.db")
        self.db = db_patcher.start()
        self.addCleanup(db_patcher.stop)

    def test_db_is_properly_called(self):
        widget = Mock()
        widgets.save_widget(widget)
        self.db.save_widget.assert_called_with(widget)

    def test_validate_exception_is_swallowed(self):
        widget = Mock()

        # Make `widget.validate` always raise `Exception`.
        widget.validate.side_effect = Exception

        widgets.save_widget(widget)


if __name__ == "__main__":
    main()
