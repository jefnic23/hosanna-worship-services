<script lang="ts">
    import Tracker from "@components/Tracker.svelte";
</script>

<nav>
    <Tracker />
</nav>

<style>
    nav {
        text-align: left;
        padding: 2rem 2rem 0.6rem;
        border-right: 1px solid #aaa;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1;
    }
</style>
