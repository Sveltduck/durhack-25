<script lang="ts">
    import Tags from "svelte-tags-input";
    import {onMount} from "svelte";

    let { name, placeholder }: {
        name: string;
        placeholder: string;
    }= $props();

    let tags: string[] = $state([]);

    let inputElement: HTMLInputElement;

    function onTagAdded() {
        console.log(tags);
        inputElement.setCustomValidity("");
    }
    function onTagRemoved() {
        if (!tags.length) {
            inputElement.setCustomValidity("Please enter at least one tag.");
        }
    }
    onMount(onTagRemoved);
</script>

<!-- Not hidden with type="hidden" so that validity message is shown -->
<input type="text" {name} value={JSON.stringify(tags)} bind:this={inputElement} />
<Tags bind:tags {placeholder} allowPaste onlyUnique {onTagAdded} {onTagRemoved} />

<style>
/* Hides the element visually but keeps it accessible to browsers and screen readers */
input {
    border: 0;
    clip: rect(0 0 0 0);
    height: 1px;
    margin: -1px;
    overflow: hidden;
    padding: 0;
    position: absolute;
    width: 1px;
}
</style>