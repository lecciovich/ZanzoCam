<script>
	export let checked = false
	export let group = ''
	export let value = void 0

	$: updateRadio(group, value)
	
	function updateRadio(group, value) {
		checked = group === value
	}	
</script>

<label>
    <input
        type="radio"
        class="collapsed"
        on:click
        bind:group={group}
        value={value}
    />
  <slot checked={checked}></slot>
</label>

<style>
	label {
		display: flex;
		align-items: center;
		user-select: none;
	}
	label > :global(*) {
		pointer-events: none;
	}
	input {
		display: none;
	}




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