<script lang="ts">
import {RangeSlider} from "svelte-range-slider-pips";
import {timeNumberToString} from "$lib/components/time-input/format";

let {
    lowerTimeName,
    upperTimeName,
    defaultLower,
    defaultUpper
}: {
    lowerTimeName: string;
    upperTimeName: string;
    defaultLower?: number;
    defaultUpper?: number;
} = $props();

let values = $state([defaultLower ?? 0, defaultUpper ?? 48]);
</script>

<input type="hidden" name={lowerTimeName} bind:value={values[0]} />
<input type="hidden" name={upperTimeName} bind:value={values[1]} />

<div>
    <RangeSlider
            min={0} max={48} step={1}
            range bind:values draggy
            float pips pipstep={6} spring={false} all="label"
            style="
                --slider-bg: #999;
                --slider-accent: #fbf;
                --range-range-inactive: #fff;
                --handle-inactive: #fff;
                --range-pip-text: #999;
                --range-pip-in-range-text: #ccc;
                --range-pip-active-text: #eee;
                --range-pip-hover-text: #fff;
                --range-float-text: #000;
            "
            formatter={timeNumberToString}
    />
</div>

<style>
    div {
        width: 30em;
    }
</style>