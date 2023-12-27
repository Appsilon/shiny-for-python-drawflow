from shiny import App, render, ui, reactive

from shiny.module import resolve_id
from htmltools import HTMLDependency

from shiny.render.transformer import (
    output_transformer,
    resolve_value_fn,
    TransformerMetadata,
    ValueFn,
)


drawflow_dep = HTMLDependency(
    "drawflow",
    "0.0.59",
    source={"subdir": "drawflow"},
    script={"src": "drawflow.min.js"},
    stylesheet={"href": "drawflow.min.css"}
)

drawflow_binding_dep = HTMLDependency(
    "drawflow_binding",
    "0.1.0",
    source={"subdir": "drawflow"},
    script={"src": "drawflowComponent.js"},
        stylesheet={"href": "drawflowComponent.css"}
)

def output_drawflow(id, height = "800px"):
    return ui.div(
        drawflow_dep,
        drawflow_binding_dep,
        # Use resolve_id so that our component will work in a module
        id=resolve_id(id),
        class_="shiny-drawflow-output",
        style=f"height: {height}",
    )

@output_transformer
async def render_drawflow(
    _meta,
    _fn,
):
    res = await resolve_value_fn(_fn)

    return {
        "message": res
    }

app_ui = ui.page_fluid(
    ui.panel_title("Custom components!"),
    ui.input_action_button(id="add_start_block", label = "Add start block"),
    ui.input_action_button(id="add_block", label = "Add intermediate block"),
    ui.input_action_button(id="add_end_block", label = "Add end block"),
    output_drawflow(id="ui_drawflow")
)


def server(input, output, session):
    @reactive.Effect
    @reactive.event(input.add_start_block)
    async def _():
        await session.send_custom_message("add_node", {"id": "ui_drawflow", "type": "start"})
    
    @reactive.Effect
    @reactive.event(input.add_block)
    async def _():
        await session.send_custom_message("add_node", {"id": "ui_drawflow", "type": "intermediate"})

    @reactive.Effect
    @reactive.event(input.add_end_block)
    async def _():
        await session.send_custom_message("add_node", {"id": "ui_drawflow", "type": "end"})

    @render_drawflow
    def ui_drawflow():
        return input.n()


app = App(app_ui, server)
