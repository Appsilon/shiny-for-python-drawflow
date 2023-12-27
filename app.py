from dataclasses import dataclass, asdict
from htmltools import HTMLDependency
from shiny import App, reactive, ui, session
from shiny.module import resolve_id
from shiny.render.transformer import (
    output_transformer,
    resolve_value_fn,
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
        id=resolve_id(id),
        class_="shiny-drawflow-output",
        style=f"height: {height}",
    )

@dataclass
class Drawflow:
    reroute: bool = True

@output_transformer
async def render_drawflow(
    _meta,
    _fn,
):
    res = await resolve_value_fn(_fn)

    return {
        "drawflow": asdict(res)
    }

async def add_node(id, node_type):
    current_session = session.get_current_session()
    await current_session.send_custom_message(
        type="add_node",
        message={
            "id": id,
            "type": node_type
        }
    )

app_ui = ui.page_fluid(
    ui.panel_title("Custom components!"),
    ui.input_action_button(id="add_start_block", label = "Add start block"),
    ui.input_action_button(id="add_intermediate_block", label = "Add intermediate block"),
    ui.input_action_button(id="add_end_block", label = "Add end block"),
    output_drawflow(id="ui_drawflow")
)


def server(input, output, session):
    @reactive.Effect
    @reactive.event(input.add_start_block)
    async def _():
        await add_node(id="ui_drawflow", node_type="start")
    
    @reactive.Effect
    @reactive.event(input.add_intermediate_block)
    async def _():
        await add_node(id="ui_drawflow", node_type="intermediate")

    @reactive.Effect
    @reactive.event(input.add_end_block)
    async def _():
        await add_node(id="ui_drawflow", node_type="end")

    @output
    @render_drawflow
    def ui_drawflow():
        drawflow = Drawflow(reroute=True)
        return drawflow


app = App(app_ui, server)
