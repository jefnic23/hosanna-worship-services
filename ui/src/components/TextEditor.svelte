<script lang="ts">
    import { eel } from "@stores";
    import { marked } from 'marked';

    let text: string = '';
    let htmlContent: string = '';
    $: text, parseMarkdown(text);

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

    async function parseMarkdown(text: string): Promise<void> {
        htmlContent = await marked.parse(text);
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
<div class='flex-row'>
    <div class='flex-col'>
        <textarea bind:value={text} on:change={handleTextChange}></textarea>
        <button on:click={handleSubmit}>Submit</button>
    </div>
    <div class='powerpoint'>{@html htmlContent}</div>
</div>


<style>
    .flex-row {
        display: flex;
        flex-direction: row;
        justify-content: center;
    }

    .flex-col {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .powerpoint {
        width: 565px;
        height: 335px;
        padding: 31.5px 16.5px;
        resize: none;
        font-size: 24px;
        font-family: 'Segoe UI';
        line-height: 1.25;
    }

    :global(.powerpoint *){
        margin: 0 0;
    }
</style>