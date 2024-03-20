<script lang="ts">
    import type { Settings } from "@interfaces/settings";
    import { eel } from "@stores";

    let settings: Settings = {};

    eel.get_settings()((s: Settings) => {
        settings = s;
    });

    const handleChange = (e: Event) => {
        settings[(e.target as HTMLInputElement).name] = (e.target as HTMLInputElement).value;
    }

    const setDir = async () => {
        let dir = await eel.set_dir()();
        settings.LOCAL_DIR = dir;
    }
</script>

{#each Object.keys(settings) as setting (setting)}
    {@const input_type = setting === "LOCAL_DIR" ? "button" : "text"}
    <span>
        <p>{setting}:</p>
        {#if input_type === "button"}
            <p>{settings[setting]}</p>
            <button on:click={setDir}>Choose Directory</button>
        {:else}
            <input type={input_type} name={setting} value={settings[setting]} on:change={handleChange} />
        {/if}
    </span>
{/each}
<button on:click={() => eel.update_settings(settings)}>Save</button>
