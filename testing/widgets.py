from . import db


def get_widgets(ids):
    return db.get_widgets(ids)


def save_widget(widget):
    try:
        widget.validate()
    except Exception:
        return None

    return db.save_widget(widget)
