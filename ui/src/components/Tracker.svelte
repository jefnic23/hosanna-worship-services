<script lang='ts'>
    import { activeTab } from "@stores";

    const handleClick = (tab: string) => {
        activeTab.set(tab);
    }
</script>

<ul>
    <li>
        <button on:click={() => handleClick('date')}>Select date</button>
    </li>
    <li>
        <button on:click={() => handleClick('liturgy')}>Select liturgy</button>
    </li>
    <li>
        <button on:click={() => handleClick('powerpoint')}>Build PowerPoint</button>
    </li>
    <li>
        <button on:click={() => handleClick('review')}>Review & confirm</button>
    </li>
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