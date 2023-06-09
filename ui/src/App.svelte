<script lang="ts">
    import DateSelector from "./components/DateSelector.svelte";
    import Planner from "./components/Planner.svelte";
    import Sidebar from "./components/Sidebar.svelte";
    import TextEditor from "./components/TextEditor.svelte";
    import { activeTab } from "./stores";
</script>

<main>
    <Sidebar />
    
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
</main>

<style>
    /* .logo {
        height: 6em;
        padding: 1.5em;
        will-change: filter;
        transition: filter 300ms;
    }
    .logo:hover {
        filter: drop-shadow(0 0 2em #646cffaa);
    }
    .logo.svelte:hover {
        filter: drop-shadow(0 0 2em #ff3e00aa);
    }
    .read-the-docs {
        color: #888;
    } */
</style>
