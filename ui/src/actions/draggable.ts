export function draggable(node: HTMLElement, data) {
    let state = data;

    node.draggable = true;
    node.style.cursor = "grab";

    function handleDragStart(e) {
        e.dataTransfer.setData("text/plain", state);
    }
}