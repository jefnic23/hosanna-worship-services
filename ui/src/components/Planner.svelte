<script lang="ts">
    import Hymn from "@components/Hymn.svelte";

    const serviceElements: {} = {
        "Confession": "Text",
        "Gathering Song": "Song",
        "Greeting": "Text",
        "Kyrie": "Text",
        "Prayer of the Day": "Text",
        "First Reading": "Text",
        "Psalm": "Text",
        "Second Reading": "Text",
        "Gospel Acclamation": "Text",
        "Gospel": "Text",
        "Sermon": "Text",
        "Song of the Day": "Song",
        "Creed": "Text",
        "Prayers of Intercession": "Text",
        "Dialogue": "Text",
        "Preface": "Text",
        "Holy, Holy, Holy": "Text",
        "Thanksgiving": "Text",
        "Lord's Prayer": "Text",
        "Communion": "Text",
        "Communion Song": "Text",
        "Communion Blessing": "Text",
        "Prayer after Communion": "Text",
        "Blessing": "Text",
        "Sending Song": "Song",
        "Dismissal": "Text",
    };

    const elementTypes: string[] = [
        "Song",
        "Text"
    ]

</script>

{#each Object.keys(serviceElements) as element (element)}
    <div class="planner-element">
        <div class="planner-element-name">{element}</div>
        {#if serviceElements[element] === "Song"}
            <Hymn />
        {:else}
            <div class="planner-element-type">{serviceElements[element]}</div>
        {/if}
    </div>
{/each}

<style>
    .planner-element {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        height: 50px;
        border-bottom: 1px solid black;
    }
</style>
