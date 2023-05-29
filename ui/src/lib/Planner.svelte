<script lang="ts">
    import Hymn from "./Hymn.svelte";

    const elements: {} = {
        'Confession': 'call_and_response',
        'Gathering Song': 'hymn',
        'Greeting': 'call_and_response',
        'Kyrie': 'congregation',
        'Prayer of the Day': 'call_and_response',
        'First Reading': 'reading',
        'Psalm': 'psalm',
        'Second Reading': 'reading',
        'Gospel Acclamation': 'congregation',
        'Gospel': 'gospel',
        'Sermon': 'title',
        'Hymn of the Day': 'hymn',
        'Creed': 'congregation',
        'Prayers of Intercession': 'intercessions',
        'Dialogue': 'call_and_response',
        'Preface': 'call_and_response',
        'Holy, Holy, Holy': 'congregation',
        'Thanksgiving': 'call_and_response',
        'Lord\'s Prayer': 'congregation',
        'Communion': 'title',
        'Communion Song': 'congregation',
        'Communion Blessing': 'call_and_response',
        'Prayer after Communion': 'call_and_response',
        'Blessing': 'call_and_response',
        'Sending Song': 'hymn',
        'Dismissal': 'call_and_response'
    }
</script>

{#each Object.keys(elements) as element}
    <div class="planner-element">
        <div class="planner-element-name">{element}</div>
        {#if elements[element] === 'hymn'}
            <Hymn />
        {:else}
            <div class="planner-element-type">{elements[element]}</div>
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