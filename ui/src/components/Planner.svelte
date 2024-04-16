<script lang="ts">
    import Hymn from "@components/Hymn.svelte";
    import Fa from "@components/Fa.svelte";
    import {
        faArrowsUpDownLeftRight,
        faX,
    } from "@fortawesome/free-solid-svg-icons";
    import { ServiceElementType } from "@interfaces/serviceElement";
    import type { ServiceElement } from "@interfaces/serviceElement";

    let serviceElements: ServiceElement[] = [
        { name: "Confession", type: ServiceElementType.Text },
        { name: "Gathering Song", type: ServiceElementType.Song },
        { name: "Greeting", type: ServiceElementType.Text },
        { name: "Kyrie", type: ServiceElementType.Text },
        { name: "Prayer of the Day", type: ServiceElementType.Text },
        { name: "First Reading", type: ServiceElementType.Text },
        { name: "Psalm", type: ServiceElementType.Text },
        { name: "Second Reading", type: ServiceElementType.Text },
        { name: "Gospel Acclamation", type: ServiceElementType.Text },
        { name: "Gospel", type: ServiceElementType.Text },
        { name: "Sermon", type: ServiceElementType.Text },
        { name: "Song of the Day", type: ServiceElementType.Song },
        { name: "Creed", type: ServiceElementType.Text },
        { name: "Prayers of Intercession", type: ServiceElementType.Text },
        { name: "Dialogue", type: ServiceElementType.Text },
        { name: "Preface", type: ServiceElementType.Text },
        { name: "Holy, Holy, Holy", type: ServiceElementType.Text },
        { name: "Thanksgiving", type: ServiceElementType.Text },
        { name: "Lord's Prayer", type: ServiceElementType.Text },
        { name: "Communion", type: ServiceElementType.Text },
        { name: "Communion Song", type: ServiceElementType.Text },
        { name: "Communion Blessing", type: ServiceElementType.Text },
        { name: "Prayer after Communion", type: ServiceElementType.Text },
        { name: "Blessing", type: ServiceElementType.Text },
        { name: "Sending Song", type: ServiceElementType.Song },
        { name: "Dismissal", type: ServiceElementType.Text },
    ];

    let dragItem: ServiceElement;

    function handleDragStart(event, item) {
        dragItem = item;
    }

    function handleDragOver(event) {
        event.preventDefault(); // Necessary to allow dropping
    }

    function handleDrop(event, item) {
        const draggingIndex = serviceElements.indexOf(dragItem);
        const targetIndex = serviceElements.indexOf(item);

        serviceElements.splice(draggingIndex, 1); // Remove the item being dragged
        serviceElements.splice(targetIndex, 0, dragItem); // Insert it before the target item

        serviceElements = [...serviceElements];

        dragItem = null; // Clear the drag item after drop
    }
</script>

<table>
    <thead>
        <tr>
            <th>Actions</th>
            <th>Service Element</th>
        </tr>
    </thead>
    <tbody>
        {#each serviceElements as serviceElement, index}
            <tr
                draggable="true"
                on:dragstart={(event) => handleDragStart(event, serviceElement)}
                on:dragover={handleDragOver}
                on:drop={(event) => handleDrop(event, serviceElement)}
            >
                <td>
                    <Fa icon={faArrowsUpDownLeftRight} color="#89b4fa" />
                    <Fa icon={faX} color="#FF0000" />
                </td>
                <td class="planner-element-name">{serviceElement.name}</td>
                {#if serviceElement.type === ServiceElementType.Song}
                    <td><Hymn /></td>
                {/if}
            </tr>
        {/each}
    </tbody>
</table>

<style>
    table {
        width: 100%;
        text-align: left;
        border-collapse: collapse;
    }

    tr {
        border-bottom: 1px solid black;
    }

    td {
        padding: 1rem 0;
    }

    /* .planner-element {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        height: 50px;
        border-bottom: 1px solid black;
    } */
</style>
