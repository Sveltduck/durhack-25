<script lang="ts">
    import Tags from "svelte-tags-input";

    let { name, placeholder }: {
        name: string;
        placeholder: string;
    }= $props();

    let tags: string[] = $state([]);
</script>

<input type="hidden" {name} value={JSON.stringify(tags)} />
<Tags bind:tags {placeholder} allowPaste onlyUnique />
