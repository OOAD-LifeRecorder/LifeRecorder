from libs.kivymd_package import *

color_list = [
    "#7fcac3",
    "#FF7F50",
    "#FFBF00",
    "#DFFF00",
    "#9FE2BF",
    "#40E0D0",
    "#6495ED",
    "#CCCCFF"
]


class EventCard(MDCardSwipe):
    def __init__(self, pk, text, category, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk
        self.delete_button = self.get_delete_button()
        self.size_hint_y=None
        self.height="30dp"
        self.add_widget(MDCardSwipeLayerBox(self.delete_button))
        color = self.get_color_by_category(category)
        self.add_widget(MDCardSwipeFrontBox(
            MDLabel(
                text=f"   {text}",
                valign="center",
                bold=True,
                padding_x="10dp"
            ),
            line_color=(0.2, 0.2, 0.2, 0.5),
            md_bg_color=color,
            size_hint=(.98, 1),
        ))

    def get_delete_button(self):
        return MDIconButton(
                    icon="trash-can",
                    pos_hint={"center_y": 0.5},
                )
    
    def get_color_by_category(self, category):
        return color_list[category]