<script lang="ts">
    import { onMount } from "svelte";
    import type { Settings } from "@interfaces/settings";
    import { eel } from "@stores";

    let settings: Settings = {};

    onMount(() => {
        eel.get_settings()((s: Settings) => {
            settings = s;
        });
    });

    let dropbox_url: string = "https://www.dropbox.com/developers/apps";

    let access_code_url: string;
    $: access_code_url = `https://www.dropbox.com/oauth2/authorize?client_id=${settings.DROPBOX_APP_KEY}&response_type=code&token_access_type=offline`;

    let screenWidth: number = screen.width;
    let screenHeight: number = screen.height;
    let windowWidth: number = 740;
    let windowHeight: number = 870;
    let left: number = screenWidth / 2 - windowWidth / 2;
    let top: number = screenHeight / 2 - windowHeight / 2;
    let windowFeatures: string = `popup,left=${left},top=${top},width=${windowWidth},height=${windowHeight}`;

    async function setDir(): Promise<void> {
        let dir = await eel.set_dir()();
        settings.LOCAL_DIR = dir;
    }
</script>

<div class="settings-group">
    <h2>Sundays and Seasons</h2>
    <div class="settings-section">
        <div class="settings-input">
            <label for="username">Username</label>
            <input type="text" name="username" bind:value={settings.USER} />
        </div>
        <div class="settings-input">
            <label for="password">Password</label>
            <input
                type="password"
                name="password"
                bind:value={settings.PASSWORD}
            />
        </div>
    </div>
</div>

<div class="settings-group">
    <h2>Dropbox</h2>
    <div class="settings-section">
        <button
            on:click={() => window.open(dropbox_url, "_blank", windowFeatures)}
        >
            Configure Dropbox
        </button>
        <div class="settings-input">
            <label for="app_key">App Key</label>
            <input
                type="text"
                name="app_key"
                bind:value={settings.DROPBOX_APP_KEY}
            />
        </div>
        <div class="settings-input">
            <label for="app_secret">Access Code</label>
            <input
                type="text"
                name="app_secret"
                bind:value={settings.DROPBOX_APP_SECRET}
            />
        </div>
        <button
            on:click={() =>
                window.open(access_code_url, "_blank", windowFeatures)}
        >
            Get access code
        </button>
        <div class="settings-input">
            <label for="refresh_token">Refresh Token</label>
            <input
                type="text"
                name="refresh_token"
                bind:value={settings.DROPBOX_REFRESH_TOKEN}
            />
        </div>
    </div>
</div>

<div class="settings-group">
    <h2>File Storage</h2>
    <div class="settings-section">
        <div class="settings-input">
            <label for="directory">Directory</label>
            <input name="directory" bind:value={settings.LOCAL_DIR} disabled />
            <button on:click={setDir}>Choose Directory</button>
        </div>
    </div>
</div>

<button on:click={() => eel.update_settings(settings)}>Save</button>

<style>
    .settings-group {
        display: flex;
        flex-direction: row;
        padding: 3rem 1rem;
        border-bottom: 1px solid white;
    }

    .settings-section {
        display: flex;
        flex-direction: column;
        flex: 2 1 0%;
    }

    .settings-input {
        display: flex;
        flex-direction: column;
    }

    h2 {
        display: flex;
        align-items: flex-start;
        width: 20%;
        flex: 1 1 0%;
    }
</style>
