import dash_mantine_components as dmc
from dash import Dash, Input, Output, callback
from transferlist_aio import TransferList

app = Dash(
    __name__,
    external_stylesheets = [
        "https://unpkg.com/@mantine/dates@7/styles.css",
        "https://unpkg.com/@mantine/code-highlight@7/styles.css",
        "https://unpkg.com/@mantine/charts@7/styles.css",
        "https://unpkg.com/@mantine/carousel@7/styles.css",
        "https://unpkg.com/@mantine/notifications@7/styles.css",
        "https://unpkg.com/@mantine/nprogress@7/styles.css",
    ]
)

initial_values = [
    [
        {"value": "react", "label": "React"},
        {"value": "ng", "label": "Angular"},
        {"value": "next", "label": "Next.js"},
        {"value": "blitz", "label": "Blitz.js"},
        {"value": "gatsby", "label": "Gatsby.js"},
        {"value": "vue", "label": "Vue"},
        {"value": "jq", "label": "jQuery"},
    ],
    [
        {"value": "sv", "label": "Svelte"},
        {"value": "rw", "label": "Redwood"},
        {"value": "np", "label": "NumPy"},
        {"value": "dj", "label": "Django"},
        {"value": "fl", "label": "Flask"},
    ],
]

app.layout = dmc.MantineProvider(
    dmc.Container(
        [
            dmc.Title("DMC 0.14 TransferList", mb=32),
            TransferList(
                aio_id="transferlist",
                value=initial_values,
                breakpoint="sm",
                # limit=5,
                listHeight=200,
                nothingFound="Nothing matches your search",
                placeholder="No items",
                radius="sm",
                searchPlaceholder="Search...",
                showTransferAll=True,
                titles=["Source", "Destination"],
                transferAllMatchingFilters=True,
            ),
            dmc.Text(id="display", py="2rem"),
        ]
    )
)


@callback(
    Output("display", "children"),
    Input(TransferList.ids.main("transferlist"), "value"),
)
def udpate_display(values):
    return dmc.SimpleGrid(
        [
            dmc.Stack(
                [
                    dmc.Text("Items in source:", fw=600),
                    dmc.List(
                        [
                            dmc.ListItem(f'{v["label"]} ({v["value"]})')
                            for v in values[0]
                        ]
                    )
                ],
            ),
            dmc.Stack(
                [
                    dmc.Text("Items in destination:", fw=600),
                    dmc.List(
                        [
                            dmc.ListItem(f'{v["label"]} ({v["value"]})')
                            for v in values[1]
                        ]
                    )
                ],
            ),
        ],
        cols=2,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
