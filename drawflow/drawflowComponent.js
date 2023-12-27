const editorMap = new Map();

class DrawFlowOutputBinding extends Shiny.OutputBinding {
    find(scope) { 
        return scope.find(".shiny-drawflow-output");
    }

    renderValue(el, payload) { 
        const editor = new Drawflow(el);
        editorMap.set(el.id, editor);

        editor.reroute = payload.drawflow.reroute;
        editor.start();
    }
}

// Register the binding
Shiny.outputBindings.register(
    new DrawFlowOutputBinding(),
    "shiny-drawflow-output"
);

Shiny.addCustomMessageHandler("add_node", function(message) {
    const editorId = message.id;
    const nodeType = message.type;
    var html = `
        <div><input type="text" df-name></div>
    `;
    var data = { "name": '' };

    var inputs = 0;
    var outputs = 1;

    switch(nodeType) {
        case 'start':
            inputs = 0;
            outputs = 1;
            break;

        case 'intermediate':
            inputs = 1;
            outputs = 1;
            break;

        case 'end':
            inputs = 1;
            outputs = 0;
            break;
    }

    editorMap.get(editorId).addNode('', inputs, outputs, 150, 300, '', data, html);
});