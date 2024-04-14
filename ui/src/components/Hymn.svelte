<script lang="ts">
    import { eel } from "@stores";
    import type { Hymn } from "@interfaces/hymn";

    let hymnNumber: string = '';
    let hymn: Hymn;

    /**
     * Sets the text to the selected text
     * @param e
     */
    function handleTextChange(e: Event): void {
        hymnNumber = (e.target as HTMLTextAreaElement).value;
    }

    /**
     * Adds the hymn to the service
     */
    function handleSubmit(): void {
        eel.get_hymn(parseInt(hymnNumber))((n: Hymn) => {
            hymn = n
        });

        hymnNumber = '';
    }
</script>

<input type='text' on:change={handleTextChange} placeholder="Enter hymn number" />
<button on:click={handleSubmit}>Submit</button>
<div>
    {#if hymn}
        <p>{hymn.title}</p>
    {/if}
</div>
