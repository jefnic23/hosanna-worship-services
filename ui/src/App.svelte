<script lang="ts">
    import DateSelector from "./lib/DateSelector.svelte";
    import Hymns from "./lib/Hymns.svelte";
    import TextEditor from "./lib/TextEditor.svelte";
    import Tracker from "./lib/Tracker.svelte";
</script>

<main>
    <Tracker />
    <DateSelector />
    <!-- <TextEditor /> -->
    <Hymns />
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
