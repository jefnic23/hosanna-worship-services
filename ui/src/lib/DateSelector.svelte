<script lang="ts">
    const eel: any = window.eel;
    eel.set_host('ws://localhost:8080');

    let delta: number = 0;
    let today: Date = new Date();
    let sunday: string = getSunday(today, delta);

    /**
     * Returns the date of the next sunday
     * @param today
     * @param delta
     */
    function getSunday(today: Date, delta: number): string {
        today.setDate(today.getDate() + ((7 - today.getDay()) % 7) + (delta * 7));
        return today.toLocaleDateString(
            'en-CA', 
            { month: '2-digit', day: '2-digit', year: 'numeric' }
        );
    }

    /**
     * Sets the date to the selected date
     * @param e
     */
    function handleDateChange(e: Event): void {
        today = new Date((e.target as HTMLInputElement).value);
        eel.print_something(today);
    }

    /**
     * Sets the date to the sunday following the current date
     */
     function handleNextSunday(): void {
        sunday = getSunday(today, delta + 1);
        today = new Date(sunday);
        eel.print_something(today);
    }
</script>

<div>
    Select day: <input type="date" bind:value={sunday} on:change={handleDateChange}/>
    <button on:click={handleNextSunday}>Next sunday</button>
    You selected: {sunday}
</div>
