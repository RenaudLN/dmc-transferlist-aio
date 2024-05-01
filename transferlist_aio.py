import json
from functools import partial
from typing import Literal

import dash_mantine_components as dmc
from dash import ALL, MATCH, Input, Output, State, callback, clientside_callback, ctx, no_update
from dash_iconify import DashIconify


def base_id(part: str, aio_id: str):
    return {"part": part, "aio_id": aio_id}


def side_id(part: str, aio_id: str, side: Literal["left", "right"]):
    return {"part": part, "aio_id": aio_id, "side": side}


class TransferList(dmc.SimpleGrid):
    """TransferList AIO component to get the DMC 0.12 working with 0.14

    :param aio_id: id of the AIO component
    :param breakpoint: Mantine breakpoint value, shifting from row to column layout
    :param limit: limit the number of items in the checklist
    :param listHeight: height of the checklist
    :param nothingFound: text to display when nothing matches the search
    :param placeholder: text to display when the checklist is empty
    :param radius: Mantine border radius for the lists
    :param searchPlaceholder: placeholder for the search input
    :param showTransferAll: show the transfer all button
    :param titles: titles of the lists
    :param transferAllMatchingFilters: Whether to transfer all or all matching filters
    :param value: initial value of the lists
    """

    class ids:
        search = partial(side_id, "__trl-search-input")
        transfer = partial(side_id, "__trl-transfer-input")
        transfer_all = partial(side_id, "__trl-transfer-all-input")
        checklist = partial(side_id, "__trl-checklist-input")
        main = partial(base_id, "__trl-main")

    def __init__(
        self,
        aio_id: str,
        breakpoint: str = None,
        limit: int = None,
        listHeight: int = 150,
        nothingFound: str = None,
        placeholder: str = None,
        radius: str = "sm",
        searchPlaceholder: str = None,
        showTransferAll: bool = True,
        titles: list[str] = None,
        transferAllMatchingFilters: bool = True,
        value: list = None,
        **kwargs
    ):
        super().__init__(
            [
                # First list
                dmc.Stack(
                    [
                        *([dmc.Text(titles[0], fw=600)] if titles else []),
                        dmc.Paper(
                            [
                                dmc.Group(
                                    [
                                        self.search_input(aio_id, "left", placeholder=searchPlaceholder),
                                        self.transfer(aio_id, "left", showTransferAll),
                                        *([self.transfer_all(aio_id, "left")] if showTransferAll else []),
                                    ],
                                    style={"alignItems": "initial"},
                                    gap=0,
                                ),
                                self.checklist(aio_id, "left", value[0], listHeight, limit),
                            ],
                            radius=radius,
                            withBorder=True,
                            style={"overflow": "hidden"},
                        ),
                    ],
                    gap="0.375rem",
                ),
                # Second list
                dmc.Stack(
                    [
                        *([dmc.Text(titles[1], fw=600)] if titles else []),
                        dmc.Paper(
                            [
                                dmc.Group(
                                    [
                                        *([self.transfer_all(aio_id, "right")] if showTransferAll else []),
                                        self.transfer(aio_id, "right", showTransferAll),
                                        self.search_input(aio_id, "right", placeholder=searchPlaceholder),
                                    ],
                                    style={"alignItems": "initial"},
                                    gap=0,
                                ),
                                self.checklist(aio_id, "right", value[1], listHeight, limit),
                            ],
                            radius=radius,
                            withBorder=True,
                            style={"overflow": "hidden"},
                        ),
                    ],
                    gap="0.375rem",
                ),
                # This input holds the actual value as well as some metadata to pass to callbacks
                dmc.JsonInput(
                    id=self.ids.main(aio_id),
                    style={"display": "none"},
                    value=value,
                    **{
                        "data-placeholder": json.dumps(placeholder),
                        "data-nothingfound": json.dumps(nothingFound),
                        "data-transferallmatchingfilters": json.dumps(transferAllMatchingFilters),
                    },
                ),
            ],
            cols={"base": 1, breakpoint: 2} if breakpoint else 2,
            spacing="md",
            **kwargs
        )

    @classmethod
    def checkbox(cls, value: dict):
        """Checkbox for the checklist.

        :param value: value of the checkbox, dict with keys label and value
        """
        return dmc.Checkbox(
            label=value["label"],
            value=value["value"],
            px="0.25rem",
            styles={
                "labelWrapper": {"flex": 1},
                "label": {"cursor": "pointer", "padding": "0.5rem 0"},
                "body": {"alignItems": "center", "gap": "0.5rem"},
            },
        )

    @classmethod
    def checklist(
        cls,
        aio_id: str,
        side: Literal["left", "right"],
        value: list[dict],
        list_height: int,
        limit: int = None,
    ):
        """Checklist in a scrollarea for each list of the transfer.

        :param aio_id: id of the AIO component
        :param side: list side
        :param value: list value, list of dicts with keys label and value
        :param list_height: height of the checklist
        :param limit: limit the number of items displayed in the checklist
        """
        if limit:
            value = value[:limit]
        return dmc.ScrollArea(
            dmc.CheckboxGroup(
                [cls.checkbox(val) for val in value],
                py="0.25rem",
                id=cls.ids.checklist(aio_id, side),
            ),
            style={"height": list_height},
            px="0.5rem",
        )

    @classmethod
    def search_input(cls, aio_id: str, side: Literal["left", "right"], **kwargs):
        """List search input.

        :param aio_id: id of the AIO component
        :param side: list side
        :param **kwargs: kwargs to pass to the TextInput
        """
        return dmc.TextInput(
            styles={
                "root": {"flex": 1},
                "input": {
                    "borderTop": "none",
                    "borderLeft": "none",
                    "borderRight": "none",
                }
            },
            radius=0,
            id=cls.ids.search(aio_id, side),
            debounce=250,
            **kwargs,
        )

    @classmethod
    def transfer_all(cls, aio_id: str, side: Literal["left", "right"]):
        """Transfer all button.

        :param aio_id: id of the AIO component
        :param side: list side
        """
        icon_side = "left" if side == "right" else "right"
        return dmc.Paper(
            dmc.UnstyledButton(
                DashIconify(icon=f"uiw:d-arrow-{icon_side}", height=12),
                style={"height": 34, "width": 34, "display": "grid", "placeContent": "center"},
                id=cls.ids.transfer_all(aio_id, side)
            ),
            withBorder=True,
            radius=0,
            style={
                "borderTop": "none",
                "borderLeft": "none",
                "borderRight": "none",
            }
        )

    @classmethod
    def transfer(cls, aio_id: str, side: Literal["left", "right"], show_transfer_all: bool):
        """Transfer button.

        :param aio_id: id of the AIO component
        :param side: list side
        :param show_transfer_all: whether the transfer all button is visible (impacts border style)
        """
        icon_side = "left" if side == "right" else "right"
        return dmc.Paper(
            dmc.UnstyledButton(
                DashIconify(icon=f"uiw:{icon_side}", height=12),
                style={"height": 34, "width": 34, "display": "grid", "placeContent": "center"},
                id=cls.ids.transfer(aio_id, side)
            ),
            withBorder=True,
            radius=0,
            style={"borderTop": "none"} | (
                {"borderRight": "none"}
                if not show_transfer_all and side == "right"
                else {}
            ) | (
                {"borderLeft": "none"}
                if not show_transfer_all and side == "left"
                else {}
            )
        )


@callback(
    Output(TransferList.ids.checklist(MATCH, MATCH), "children"),
    Output(TransferList.ids.checklist(MATCH, MATCH), "value"),
    Input(TransferList.ids.search(MATCH, MATCH), "value"),
    State(TransferList.ids.main(MATCH), "value"),
    State(TransferList.ids.main(MATCH), "data-nothingfound"),
    State(TransferList.ids.main(MATCH), "data-placeholder"),
    State(TransferList.ids.checklist(MATCH, MATCH), "value"),
    prevent_initial_call=True,
)
def filter_checklist(
    search: str,
    values: list[list[dict]],
    nothing_found: str,
    placeholder: str,
    selection: list[str],
):
    """Filter the list on search."""
    if not ctx.triggered_id:
        return no_update, no_update

    value = values[0] if ctx.triggered_id["side"] == "left" else values[1]
    filtered = [v for v in value if not search or search.lower() in v["label"].lower()]
    children = None
    filtered_values = [f["value"] for f in filtered]
    updated_selection = [s for s in (selection or []) if s in filtered_values]
    if filtered:
        children = [TransferList.checkbox(val) for val in filtered]
    elif search and nothing_found:
        children = dmc.Text(json.loads(nothing_found), p="0.5rem", c="dimmed")
    elif not search and placeholder:
        children = dmc.Text(json.loads(placeholder), p="0.5rem", c="dimmed")
    return children, updated_selection


@callback(
    Output(TransferList.ids.main(MATCH), "value"),
    Output(TransferList.ids.checklist(MATCH, ALL), "children", allow_duplicate=True),
    Output(TransferList.ids.checklist(MATCH, ALL), "value", allow_duplicate=True),
    Output(TransferList.ids.search(MATCH, ALL), "value", allow_duplicate=True),
    Input(TransferList.ids.transfer(MATCH, ALL), "n_clicks"),
    Input(TransferList.ids.transfer_all(MATCH, ALL), "n_clicks"),
    State(TransferList.ids.checklist(MATCH, ALL), "value"),
    State(TransferList.ids.search(MATCH, ALL), "value"),
    State(TransferList.ids.main(MATCH), "value"),
    State(TransferList.ids.main(MATCH), "data-placeholder"),
    State(TransferList.ids.main(MATCH), "data-transferallmatchingfilters"),
    prevent_initial_call=True,
)
def transfer_values(
    trigger1: list[int],
    trigger2: list[int],
    selection: list[list[str]],
    search: list[str],
    current_value: list[list[dict]],
    placeholder: str,
    transfer_matching: str,
):
    """Transfer items from one list to the other."""
    if not (ctx.triggered_id and (any(trigger1) or any(trigger2))):
        return no_update, no_update, no_update, no_update

    side = ctx.triggered_id["side"]
    # Transfer selected items when clicking the transfer button
    if ctx.triggered_id["part"] == TransferList.ids.transfer("", "")["part"]:
        transferred = selection[0] if side == "left" else selection[1]
    # Transfer all items when clicking the transfer all button
    else:
        # Filter out items that don't match the search if transfer_matching is set
        if json.loads(transfer_matching):
            search_ = search[0 if side == "left" else 1]
            transferred = [
                v["value"] for v in current_value[0 if side == "left" else 1]
                if not search_ or search_.lower() in v["label"].lower()
            ]
        else:
            transferred = [v["value"] for v in current_value[0 if side == "left" else 1]]

    if not transferred:
        return no_update, [no_update] * 2, [no_update] * 2, [no_update] * 2

    # Update the value
    if side == "left":
        new_value = [
            [v for v in current_value[0] if v["value"] not in transferred],
            current_value[1] + [v for v in current_value[0] if v["value"] in transferred],
        ]
    else:
        new_value = [
            current_value[0] + [v for v in current_value[1] if v["value"] in transferred],
            [v for v in current_value[1] if v["value"] not in transferred],
        ]

    # Create the new checkboxes or placeholder texts
    placeholder = json.loads(placeholder)
    new_children = [
        [TransferList.checkbox(v) for v in new_value[0]]
        if new_value[0]
        else dmc.Text(placeholder, p="0.5rem", c="dimmed"),
        [TransferList.checkbox(v) for v in new_value[1]]
        if new_value[1]
        else dmc.Text(placeholder, p="0.5rem", c="dimmed"),
    ]

    return new_value, new_children, [[]] * 2, [""] * 2


# Gray out the transfer button when nothing is selected
clientside_callback(
    """(selection, style) => {
        return {
            ...style,
            color: !!selection.length ? null : "gray",
            cursor: !!selection.length ? "pointer" : "default",
        }
    }""",
    Output(TransferList.ids.transfer(MATCH, MATCH), "style"),
    Input(TransferList.ids.checklist(MATCH, MATCH), "value"),
    State(TransferList.ids.transfer(MATCH, MATCH), "style"),
)


# Gray out the transfer all button when nothing can be transferred
clientside_callback(
    """(filtered, style) => {
        const disabled = !filtered || !filtered.length
        return {
            ...style,
            color: !disabled ? null : "gray",
            cursor: !disabled ? "pointer" : "default",
        }
    }""",
    Output(TransferList.ids.transfer_all(MATCH, MATCH), "style"),
    Input(TransferList.ids.checklist(MATCH, MATCH), "children"),
    State(TransferList.ids.transfer_all(MATCH, MATCH), "style"),
)
