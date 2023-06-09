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
        {#if $activeTab === 'date'}
            <DateSelector isActive={true} />
        {:else if $activeTab === 'liturgy'}
            <TextEditor isActive={true} />
        {:else if $activeTab === 'powerpoint'}
            <Planner isActive={true} />
        {:else if $activeTab === 'review'}
            <Planner isActive={true} />
        {:else}
            <DateSelector isActive={true} />
        {/if}
    </div>
</main>

<style>
    .container {
        display: grid;
        grid-template-rows: 1fr;
        grid-template-columns: 1fr;
    }
</style>
