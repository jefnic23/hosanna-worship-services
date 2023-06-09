<script lang="ts">
    import DateSelector from "./components/DateSelector.svelte";
    import Planner from "./components/Planner.svelte";
    import Sidebar from "./components/Sidebar.svelte";
    import TextEditor from "./components/TextEditor.svelte";
    import { activeTab } from "./stores";
</script>

<main>
    <Sidebar />
    
    <div class='container'>
        <div class='container-item'>
            {#if $activeTab === 'date'}
                <DateSelector />
            {:else if $activeTab === 'liturgy'}
                <TextEditor />
            {:else if $activeTab === 'powerpoint'}
                <Planner />
            {:else if $activeTab === 'review'}
                <Planner />
            {:else}
                <DateSelector />
            {/if}
        </div>
    </div>
</main>

<style>
    .container {
        display: grid;
        grid-template-rows: 1fr;
        grid-template-columns: 1fr;
    }

    .container-item {
        grid-row: 1;
        grid-column: 1;
    }
</style>
