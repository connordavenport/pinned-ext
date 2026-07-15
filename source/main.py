import AppKit
from mojo.extensions import getExtensionDefault
from mojo.subscriber import Subscriber, registerRoboFontSubscriber

PINNED_HEADER = "􀎧 Pinned"
EXTENSION_KEY = "tools.programme.ext_pin"


def rebuildMenu(pinned: list[str] = []) -> None:

    menubar = AppKit.NSApp().mainMenu()
    extensionsItem = menubar.itemWithTitle_("Extensions")
    extensionsMenu = extensionsItem.submenu()
    _array = list(extensionsMenu.itemArray().copy())
    item_array = AppKit.NSMutableArray.alloc().init()
    header = _array[:2]  # header will always be Mechanic + seperator
    _array = _array[2:]
    pinnedObjects = [
        p for p in _array if p.title() in pinned
    ]  # get the objects from the current menu that will be pinned
    for temp in _array:
        if temp.title() == PINNED_HEADER:
            _array.remove(temp)
        elif temp.isSeparatorItem():
            _array.remove(temp)
    for i in header[:2]:
        item_array.addObject_(i)
    if pinned:
        item_array.addObject_(AppKit.NSMenuItem.sectionHeaderWithTitle_(PINNED_HEADER))
        for p in pinnedObjects:
            item_array.addObject_(p)
        item_array.addObject_(AppKit.NSMenuItem.separatorItem())

    _array = sorted(_array, key=lambda x: x.title())
    for item in _array:
        if item in item_array:
            pass
        else:
            item_array.addObject_(item)
    built_menu = AppKit.NSArray.alloc().initWithArray_(item_array)
    extensionsMenu.setItemArray_(built_menu)


class PinnedSubscriber(Subscriber):
    def build(self):
        pass

    def roboFontDidFinishLaunching(self, notification):
        rebuildMenu(getExtensionDefault(EXTENSION_KEY, []))


if __name__ == "__main__":
    registerRoboFontSubscriber(PinnedSubscriber)
