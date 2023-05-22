<script lang="ts">
    import { eel } from "../main";

    let today: Date = new Date();
    let formattedDate: string = formatDate(today);

    /**
     * Formats the date to the format YYYY-MM-DD
     * @param date
     */
    function formatDate(date: Date): string {
        return date.toISOString().slice(0, 10);
    }

    /**
     * Returns the date of the next sunday
     */
    function getNextSunday(): void {
        today.setDate(today.getDate() + ((0 - today.getDay()) % 7) + 7);
    }

    /**
     * Sets the date to the selected date
     * @param e
     */
    function handleDateChange(e: Event): void {
        let dateParts: string[] = (e.target as HTMLInputElement).value.split('-');
        today = new Date(parseInt(dateParts[0]), parseInt(dateParts[1]) - 1, parseInt(dateParts[2]));
        formattedDate = formatDate(today);
    }

    /** 
     * Sets the date to the sunday following the current date
     */
     function handleNextSunday(): void {
        getNextSunday();
        formattedDate = formatDate(today);
    }

    /**
     * Prints the date
     */
    function handleSubmit(): void {
        eel.set_date(formatDate(today))();
    }
</script>

<div>
    Select day: <input type="date" bind:value={formattedDate} on:change={handleDateChange}/>
    <button on:click={handleNextSunday}>Next sunday</button>
    <button on:click={handleSubmit}>Submit</button>
</div>
