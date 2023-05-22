<script lang="ts">
    import { eel } from "../main";

    let delta: number = 0;
    let today: Date = new Date();
    let formattedDate: string = formatDate(today);
    let sunday: string = getSunday(today, delta);

    /**
     * Formats the date to the format MM/DD/YYYY
     * @param date
     */
    function formatDate(date: Date): string {
        return date.toLocaleDateString(
            'en-CA', 
            { month: '2-digit', day: '2-digit', year: 'numeric' }
        );
    }

    /**
     * Returns the date of the next sunday
     * @param today
     * @param delta
     */
    function getSunday(today: Date, delta: number): string {
        today.setDate(today.getDate() + ((7 - today.getDay()) % 7) + (delta * 7));
        return formatDate(today);
    }

    /**
     * Sets the date to the selected date
     * @param e
     */
    function handleDateChange(e: Event): void {
        today = new Date((e.target as HTMLInputElement).value);
        eel.print_something(formatDate(today));
    }

    /**
     * Sets the date to the sunday following the current date
     */
     function handleNextSunday(): void {
        sunday = getSunday(today, delta + 1);
        today = new Date(sunday);
        formattedDate = formatDate(today);
        eel.print_something(formatDate(today));
    }

    /**
     * Prints the date
     */
    function handleSubmit(): void {
        eel.set_date(formatDate(today));
    }
</script>

<div>
    Select day: <input type="date" bind:value={formattedDate} on:change={handleDateChange}/>
    <button on:click={handleNextSunday}>Next sunday</button>
    <button on:click={handleSubmit}>Submit</button>
</div>
