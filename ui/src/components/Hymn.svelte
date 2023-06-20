<script lang="ts">
    import { eel } from "@stores";
    import type { Hymn } from "@interfaces/hymn";

    let hymn: string = '';
    let hymns: Hymn[] = [];

    /**
     * Sets the text to the selected text
     * @param e
     */
    function handleTextChange(e: Event): void {
        hymn = (e.target as HTMLTextAreaElement).value;
    }

    /**
     * Adds the hymn to the service
     */
    function handleSubmit(): void {
        eel.add_hymn(parseInt(hymn))((n: Hymn[]) => {
            hymns = n
        });

        hymn = '';
    }
</script>

<input type='text' on:change={handleTextChange} placeholder="Enter hymn number" />
<button on:click={handleSubmit}>Submit</button>
<div>
    {#each hymns as hymn (hymn.number)}
        <p>{hymn.title}</p>
        <p>{hymn.number}</p>
    {/each}
</div>
