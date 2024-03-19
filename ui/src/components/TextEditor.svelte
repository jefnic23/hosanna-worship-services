<script lang="ts">
    import { eel } from "@stores";
    import { marked } from 'marked';

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

    textarea {
        width: 565px;
        height: 335px;
        padding: 31.5px 16.5px;
        resize: none;
        font-size: 24px;
        font-family: 'Segoe UI';
    }
</style>