<script lang="ts">
    let {
        name,
        value = $bindable(),
        min = "00:00",
        max = "23:30",
        required = true,
    }: {
        name: string;
        value?: string;
        min?: string;
        max?: string;
        required?: boolean;
    } = $props();

    function clampTime() {
        const time = value as string; // assert defined
        // Clamp to min/max
        if (time < min) return min;
        if (time > max) return max;
        // Clamp to nearest half hour
        const [hours, minutes] = time.split(":").map(Number);
        value = minutes > 30
            ? `${String(hours + 1).padStart(2, "0")}:00`
            : `${String(hours).padStart(2, "0")}:30`;
    }
</script>

<input
    type="time"
    bind:value
    {name}
    {min}
    {max}
    {required}
    step="1800"
    onchange={clampTime}
/>
