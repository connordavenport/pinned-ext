import ezui
import AppKit
from mojo.extensions import getExtensionDefault, setExtensionDefault

from main import rebuildMenu, PINNED_HEADER, EXTENSION_KEY


class PinnedController(ezui.WindowController):
    def build(self):

        self.pinned = getExtensionDefault(EXTENSION_KEY, [])

        menubar = AppKit.NSApp().mainMenu()
        self.extensions_menu = menubar.itemWithTitle_("Extensions").submenu()
        self._array = list(self.extensions_menu.itemArray().copy())

        extensions_list = sorted(
            [
                i.title()
                for i in list(self.extensions_menu.itemArray().copy())
                if i.title() not in ["Mechanic", "", PINNED_HEADER]
            ]
        )

        items = [
            dict(
                imageValue=ezui.makeImage(symbolName="circle.dotted")
                if item not in self.pinned
                else ezui.makeImage(symbolName="pin.fill"),
                extNameValue=item,
                pinnedValue=item in self.pinned,
            )
            for item in extensions_list
        ]

        content = """
        | ----------------- | @table
        ( Pin Extensions )    @pinButton
        """
        descriptionData = dict(
            table=dict(
                items=items,
                showColumnTitles=False,
                columnDescriptions=[
                    dict(
                        identifier="imageValue",
                        title="Image",
                        width=30,
                        cellDescription=dict(cellType="Image"),
                    ),
                    dict(
                        identifier="pinnedValue",
                        title="pinned",
                        width=30,
                        editable=True,
                        cellDescription=dict(
                            cellType="Checkbox",
                        ),
                    ),
                    dict(
                        identifier="extNameValue",
                        title="extName",
                    ),
                ],
            )
        )
        self.w = ezui.EZWindow(
            title="Pinned",
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(400, 500),
        )

    def pinButtonCallback(self, sender):
        rebuildMenu(self.pinned)

    def tableEditCallback(self, sender):
        self.pinned = []
        for i, item in enumerate(sender.get()):
            temp_edit = item
            if item.get("pinnedValue"):
                temp_edit["imageValue"] = ezui.makeImage(symbolName="pin.fill")
                self.pinned.append(temp_edit["extNameValue"])
            else:
                temp_edit["imageValue"] = ezui.makeImage(symbolName="circle.dotted")
            self.w.getItem("table").setItem(i, temp_edit)
        setExtensionDefault(EXTENSION_KEY, self.pinned)

    def started(self):
        self.w.open()


if __name__ == "__main__":
    PinnedController()
