export function draggable(node: HTMLElement, data: any) {
    let state: any = data;

    node.draggable = true;
    node.style.cursor = "grab";

    function handleDragStart(e: DragEvent) {
        e.dataTransfer.setData("text/plain", data);
    }

    node.addEventListener("dragstart", handleDragStart);

    return {
        update(data: any) {
            state = data;
        },
        destroy() {
            node.removeEventListener("dragstart", handleDragStart);
        }
    }
}

export function dropzone(node: HTMLElement, options: any) {
    let state: any = {
        dropEffect: "move",
        dragOverClass: "droppable",
        ...options
    }

    function handleDragEnter(e: DragEvent) {
        (e.target as Element).classList.add(state.dragOverClass);
    }

    function handleDragLeave(e: DragEvent) {
        (e.target as Element).classList.remove(state.dragOverClass);
    } 

    function handleDragOver(e: DragEvent) {
        e.preventDefault();
        e.dataTransfer.dropEffect = state.dropEffect;
    }

    function handleDrop(e: DragEvent) {
        e.preventDefault();
        (e.target as Element).classList.remove(state.dragOverClass);
        const data = e.dataTransfer.getData("text/plain");
        state.onDrop(data, e);
    }

    node.addEventListener("dragenter", handleDragEnter);
    node.addEventListener("dragleave", handleDragLeave);
    node.addEventListener("dragover", handleDragOver);
    node.addEventListener("drop", handleDrop);

    return {
        update(options: any) {
            state = {
                dropEffect: "move",
                dragOverClass: "droppable",
                ...options
            }
        },
        destroy() {
            node.removeEventListener("dragenter", handleDragEnter);
            node.removeEventListener("dragleave", handleDragLeave);
            node.removeEventListener("dragover", handleDragOver);
            node.removeEventListener("drop", handleDrop);
        }
    }
}