<script lang='ts'>
    import type { Page } from "@interfaces/page";
    import { activeTab } from "@stores";

    const pages: Page[] = [
        { name: 'date', description: 'Select date' },
        { name: 'liturgy', description: 'Select liturgy' },
        { name: 'powerpoint', description: 'Build PowerPoint' },
        { name: 'review', description: 'Review & confirm' }
    ]

    const handleClick = (tab: string) => {
        activeTab.set(tab);
    }
</script>

<ul>
    {#each pages as page (page.name)}
        <li>
            <button on:click={() => handleClick(page.name)}>{page.description}</button>
        </li>
    {/each}
</ul>

<style>
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
</style>