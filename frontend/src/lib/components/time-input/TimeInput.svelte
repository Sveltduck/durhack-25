<script lang="ts">
    import {RangeSlider} from "svelte-range-slider-pips";
    import {timeNumberToString} from "$lib/components/time-input/format";

    let {
        name,
        defaultValue
    }: {
        name: string;
        defaultValue?: number;
    } = $props();

    let value = $state(defaultValue ?? 0);
</script>

<input type="hidden" {name} bind:value={value} />

<div>
    <RangeSlider
            min={0} max={47} step={1}
            bind:value
            float pips pipstep={6} spring={false} all="label"
            formatter={timeNumberToString}
    />
</div>

<style>
    div {
        margin: 0 .5em;
    }
</style>