<script lang="ts">
    import { eel } from "@stores";

    let text: string = '';

    let liturgies: string[] = [];
    eel.list_liturgies()((n: string[]) => {
        liturgies = n;
    });

    /**
     * Sets the text to the selected text
     * @param e
     */
    function handleTextChange(e: Event): void {
        text = (e.target as HTMLTextAreaElement).value;
    }

    /**
     * Prints the text
     */
    function handleSubmit(): void {
        eel.print_something(text);
    }
</script>

{#each liturgies as liturgy (liturgy)}
    <p>{liturgy}</p>
{/each}
<div class='flex'>
    <textarea bind:value={text} on:change={handleTextChange}></textarea>
    <button on:click={handleSubmit}>Submit</button>
</div>

<style>
    .flex {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
</style>