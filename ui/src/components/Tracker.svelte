<script lang='ts'>
    import { activeTab } from "../stores";

    const handleClick = (tab: string) => {
        activeTab.set(tab);
    }
</script>

<ul>
    <li>
        <span on:click={() => handleClick('date')}>Select date</span>
    </li>
    <li>
        <span on:click={() => handleClick('liturgy')}>Select liturgy</span>
    </li>
    <li>
        <span on:click={() => handleClick('powerpoint')}>Build PowerPoint</span>
    </li>
    <li>
        <span on:click={() => handleClick('review')}>Review & confirm</span>
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

    span:hover {
        cursor: pointer;
    }
</style>