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

<input type="text" hidden {name} value={JSON.stringify(tags)} bind:this={inputElement} />
<Tags bind:tags {placeholder} allowPaste onlyUnique {onTagAdded} {onTagRemoved} />
