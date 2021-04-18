<script lang="ts">
    export let name = '';
    export let password = '';
    export let show_password = false;

    function toogle_visibility() {
        show_password = !show_password
    }
</script>

<div class="flex flex-row">

    {#if show_password}
    <input name="{name}" type="text" bind:value="{password}" class="flex-grow input-borders">
    {:else}
    <input name="{name}" type="password" bind:value="{password}" class="flex-grow input-borders">
    {/if}
    <button on:click={toogle_visibility} 
            type="button" 
            class="text-white bg-blue-500 hover:bg-blue-700 py-2 px-4 rounded-md shadow-md"
            >Mostra</button> 
</div>