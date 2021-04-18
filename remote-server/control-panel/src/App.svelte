<script lang="ts">

	import PasswordInput from "./components/PasswordInput.svelte";
	import ToggleButton from "./components/ToggleButton.svelte";
	import Tailwind from "./Tailwind.svelte";

	let version = "v0.7.1";

	let server_protocol = "HTTP";

	let nameA = null;
	let nameB = null;
	let choice = "a"

</script>

<style global lang="postcss">
	/* FIXME */
	p, h1, h2, h3, h4, input, span, button, a, label {
		font-family: 'Raleway' !important;
	}
    .input-borders {
        @apply py-1;
        @apply px-2;
        @apply outline-none;
		@apply focus:outline-none;
        @apply rounded-md;
        @apply border;
        @apply border-blue-200;
        @apply focus:border-blue-400;
    }
	label {
		@apply text-blue-800;
	}
</style>


<Tailwind></Tailwind>

<div>

	<!--input type=radio bind:group={choice} value={'A'}>
	<input type=radio bind:group={choice} value={'B'}>

	{#if choice === "A"}
	<p>Name for A: {nameA}</p>
	<input id="name" type="text" name="name" bind:value={nameA}/>
	{:else if choice === "B"}
	<p>Name for B: {nameB}</p>
	<input id="name" type="text" name="name" bind:value={nameB}/>
	{:else }
	<p>Select a radio!</p>
	{/if} -->


	<form class="container flex flex-col items-center gap-y-5
				max-w-screen-md 
				mx-auto my-10 p-10 
				bg-white rounded-lg shadow-lg">

		<img src="logos/logo-zanzocam.png" alt="Logo ZANZOCAM" width="150px">
		<p class="text-sm text-blue-400">{version}</p>

		<h1 class="text-5xl text-blue-900 font-raleway">Impostazioni</h1>


		<div class="flex flex-col item-grow gap-y-2
					p-10 w-full
					rounded-lg shadow-lg border border-gray-200">

			<div class="flex flex-row gap-x-10 mb-5">
				<h3 class="text-3xl text-blue-500">Server:</h3>

				{#each ["HTTP", "FTP"] as protocol}
					<Toggle type='radio' bind:group={selectedProtocol} value={protocol} let:checked={checked}>
						{item}
					</Toggle>
				{/each}

				<ToggleButton name="server__protocol" buttons={} ></ToggleButton>
			</div>
				
			{#if server_protocol == "HTTP"}
			<div id="server_protocol_HTTP" class="hidden">
				<label for="server__url">URL del server:</label>
				<input type="text" name="server__url">
			</div>
			{:else if server_protocol == "FTP"}
			<div id="server_protocol_FTP-vars" class="hidden">
				<label for="server__hostname" >Hostname:</label>
				<input name="server__hostname" type="text">

				<label for="server__subfolder">Sottocartella (se necessaria):</label>
				<input name="server__subfolder" type="text" >

				<label for="server__tls">Usa TLS</label>
				<input name="server__tls" type="checkbox" checked>
			</div>
			{/if}

			<label for="server__username">Username (se necessario):</label>
			<input name="server__username" type="text" class="input-borders">
			
			<label for="server__password">Password (se necessaria):</label>
			<PasswordInput name='server__password' />
			
		</div>

		<!--h3>Orario:</h3>

			<label>Inizia a scattare alle:</label>
			<input name="time__start_activity" type="text" placeholder="00:01">

			<label class="label-inline">Smetti di scattare alle:</label>
			<input name="time__stop_activity" type="text" placeholder="23:59">

			<label class="label-inline">Frequenza scatti:</label>
			<select name="time__frequency">
				<option value=0  >Manuale</option>
				<option value=5 >Ogni 5 minuti</option>
				<option value=10 >Ogni 10 minuti</option>
				<option value=15 >Ogni 15 minuti</option>
				<option value=20 >Ogni 20 minuti</option>
				<option value=30 >Ogni 30 minuti</option>
				<option value=60 selected>Ogni ora</option>
				<option value=120 >Ogni 2 ore</option>
				<option value=240 >Ogni 4 ore</option>
				<option value=480 >Ogni 8 ore</option>
			</select>

			

			<details>
				<summary>Modalita' esperto (configuratione crontab diretta)</summary>
				
				<p>
				<br>
				<b>NOTA BENE:</b> se anche uno solo di questi campi contiene un valore, 
				la frequenza definita sopra verra' ignorata.
				</p>
				<div class="row">
					<div class="column">
						<label class="label-inline">Minuti:</label>
						<input type="text" placeholder="*"  name="crontab__minute">
					</div>
					<div class="column">
						<label class="label-inline">Ora:</label>
						<input type="text" placeholder="*"  name="crontab__hour">
					</div>
					<div class="column">
						<label class="label-inline">Giorno:</label>
						<input type="text" placeholder="*"  name="crontab__day">
					</div>
					<div class="column">
						<label class="label-inline">Mese:</label>
						<input type="text" placeholder="*"  name="crontab__month">
					</div>
					<div class="column">
						<label class="label-inline">G. settimana:</label>
						<input type="text" placeholder="*"  name="crontab__weekday">
					</div>
				</div>
			</details-->
			
		<button class='text-white text-2xl bg-blue-500 hover:bg-blue-700 py-3 px-6 rounded-md shadow-md'>Salva</button>
	</form>
</div>
