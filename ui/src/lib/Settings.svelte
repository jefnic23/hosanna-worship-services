<script lang="ts">
    import { eel } from "../main";
    import { type Settings } from "./types/settings";

    let settings: Settings = {};

    eel.get_settings()((s: Settings) => {
        settings = s;
    });

    const handleChange = (e: Event) => {
        settings[(e.target as HTMLInputElement).name] = (e.target as HTMLInputElement).value;
    }

    async function getDir() {
        const handleDir = await window.showDirectoryPicker();
        const dir = await handleDir.getDirectory();
        const path = dir.path;
        settings["LOCAL_DIR"] = path;
    }
</script>

{#each Object.keys(settings) as setting}
    {@const input_type = setting === "LOCAL_DIR" ? "button" : "text"}
    <span>
        <p>{setting}:</p>
        {#if input_type === "button"}
            <button on:click={getDir}>Choose Directory</button>
        {:else}
            <input type={input_type} name={setting} value={settings[setting]} on:change={handleChange} />
        {/if}
    </span>
{/each}
<button on:click={() => eel.update_settings(settings)}>Save</button>
