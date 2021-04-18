<script lang="ts">

    export let name: string;
    export let buttons: string[];
    export let selected: string;

    function select(e, buttonName){
        buttonName = e.target.value === "true"
        selected = buttonName;
    }
</script>

<style>


.toggle {
    @apply flex;
    @apply overflow-hidden;
}

.toggle input {
  position: absolute !important;
  clip: rect(0, 0, 0, 0);
  height: 1px;
  width: 1px;
  border: 0;
  overflow: hidden;
}

.toggle label {
    @apply bg-gray-300;
    @apply text-white;
    @apply py-2;
    @apply px-6;
    @apply transition-all;
    @apply cursor-pointer;
}

.toggle input:checked + label {
    @apply bg-blue-500;
}

</style>

<div>
    <div class="flex flex-row max-w-min gap-0 rounded overflow-hidden">
        {#each buttons as button }
            <div class="toggle">
                <input type="radio" id="radio-{name}-{button}" value="{button}" name="{name}" on:change="{select}">
                <label for="radio-{name}-{button}">{button}</label>
            </div>
        {/each}
    </div>
</div>