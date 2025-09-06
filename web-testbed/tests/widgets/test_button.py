# Handled differently in real testing with get_module()

from pytest import approx, fixture

# from ..tests_backend.widgets.button import ButtonProbe
# from ..tests_backend.proxies.button_proxy import ButtonProxy
from tests.data import TEXTS
from tests.tests_backend.proxies.button_proxy import ButtonProxy


@fixture
async def widget():
    return ButtonProxy()


async def test_text(widget, probe):
    "The text displayed on a button can be changed"
    initial_height = probe.height

    for text in TEXTS:
        widget.text = text

        # no-op
        # await probe.redraw(f"Button text should be {text}")

        # Text after a newline will be stripped.
        assert isinstance(widget.text, str)
        expected = str(text).split("\n")[0]
        assert widget.text == expected
        assert probe.text == expected
        # GTK rendering can result in a very minor change in button height
        assert probe.height == approx(initial_height, abs=1)


async def test_icon(widget, probe):
    assert probe.text == "Hello"
    assert widget.icon is None
    initial_height = probe.height

    widget.icon = "resources/icons/red"

    assert probe.text == ""
    assert widget.icon is not None
    # time.sleep(5)
    assert probe.height > initial_height

    widget.text = "Goodbye"

    assert probe.text == "Goodbye"
    assert widget.icon is None
    assert probe.height == initial_height

    """
    async def test_icon(widget, probe):

    # Initial button is a text button.
    assert probe.text == "Hello"
    assert widget.icon is None
    probe.assert_no_icon()
    initial_height = probe.height

    # Set an icon
    widget.icon = "resources/icons/red"
    await probe.redraw("Button is now an icon button")

    # Text has been removed
    assert probe.text == ""
    # Icon now exists
    assert widget.icon is not None
    probe.assert_icon_size() # Should be 32 x 32
    # Button is now taller.
    assert probe.height > initial_height

    # Move back to text
    widget.text = "Goodbye"
    await probe.redraw("Button is a text button again")

    # Text has been added
    assert probe.text == "Goodbye"
    # Icon no longer exists
    assert widget.icon is None
    probe.assert_no_icon()
    # Button is original size
    assert probe.height == initial_height
    """
