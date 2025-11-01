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
            style="
                --slider-bg: #999;
                --handle-inactive: #fff;
                --range-pip-text: #999;
                --range-pip-active-text: #eee;
                --range-pip-hover-text: #fff;
            "
            formatter={timeNumberToString}
    />
</div>

<style>
    div {
        width: 30em;
    }
</style>