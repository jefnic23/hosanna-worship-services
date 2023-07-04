<script lang="ts">
    import DateSelector from "@components/DateSelector.svelte";
    import Planner from "@components/Planner.svelte";
    import Settings from "@components/Settings.svelte";
    import TextEditor from "@components/TextEditor.svelte";
    import type { Page } from "@interfaces/page";
    import { activeTab } from "@stores";
    import { fly } from "svelte/transition";

    const pages: Page[] = [
        { name: 'date', description: 'Select date', content: DateSelector },
        { name: 'liturgy', description: 'Select liturgy', content: TextEditor },
        { name: 'powerpoint', description: 'Build PowerPoint', content: Planner },
        { name: 'review', description: 'Review & confirm', content: Settings }
    ]
</script>

<main>
    <nav>
        <ul>
            {#each pages as page (page.name)}
                <li>
                    <button on:click={() => activeTab.set(page.name)}>{page.description}</button>
                </li>
            {/each}
        </ul>
    </nav>
    <div class="container">
        {#each pages as page (page.name)}
            {#if $activeTab === page.name}
                <div 
                    class="container-item"
                    in:fly="{{ x: -500, duration: 300 }}"
                    out:fly="{{ x: 500, duration: 300 }}"
                >
                    <svelte:component this={page.content} />
                </div>
            {/if}
        {/each}
    </div>
</main>

<style>
    main {
        display: grid;
        grid-template-columns: 250px 5fr;
        height: 100vh;
        position: fixed;
    }

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

    ul {
        padding-left: 1.2rem;
        list-style: circle;
    }

    li {
        margin: 1rem 0;
    }

    button:hover {
        cursor: pointer;
    }

    .container {
        display: grid;
        grid-template-rows: 1fr;
        grid-template-columns: 1fr;
        min-height: 100vh;
        margin-left: 250px;
        width: calc(100vw - 250px);
        overflow-y: scroll;
        overflow-x: hidden;
    }

    .container-item {
        grid-row: 1;
        grid-column: 1;
        padding: 1rem;
        margin: auto;
    }
</style>
