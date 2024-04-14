<script lang="ts">
    import { eel } from "@stores";
    import { marked } from "marked";

    marked.use({
        gfm: true,
        breaks: true
    });

    export let text: string = "";
    let htmlContent: string[] = [""];

    $: text, parseMarkdown(text);

    /**
     * Converts text into markdown
     * @param text
     */
    async function parseMarkdown(text: string): Promise<void> {
        let slides = text.split("<br>");
        htmlContent = await Promise.all(
            slides.map((slide) => marked.parse(slide)),
        );
    }

    /**
     * Prints the text
     */
    function handleSubmit(): void {
        eel.print_something(text);
    }
</script>

<div class="flex-row">
    <div class="flex-col">
        <textarea bind:value={text}></textarea>
        <button on:click={handleSubmit}>Submit</button>
    </div>
    <div class="powerpoint">
        {#each htmlContent as slide}
            <div class="slides">{@html slide}</div>
        {/each}
    </div>
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
        display: flex;
        flex-direction: column;
        row-gap: 1rem;
    }

    .slides {
        width: 565px;
        height: 335px;
        padding: 31.5px 16.5px;
        resize: none;
        font-size: 24px;
        font-family: "Segoe UI";
        line-height: 1.25;
        border: 1px white solid;
    }

    :global(.slides *) {
        margin: 0 0;
    }
</style>
