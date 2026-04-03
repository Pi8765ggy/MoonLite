<script setup>
	import { ref, onMounted } from "vue"
	
	// moon_img only contains the img url
	// moon_data contains the rest of the important info
	const moon_img = ref({})
	const moon_data = ref({})
	const loadingData = ref(true)
	const error = ref(false)

	onMounted(async () => {
		try {
			const resp = await fetch("/api/moon_img")
			if (!resp.ok) {
				// Catches a bad response code from the flask api
				console.error(resp.status)
				error.value = true
				return
			}
			const data = await resp.json()
			moon_img.value = data

			const resp1 = await fetch("/api/moon_data")
			if (!resp1.ok) {
				console.error(resp1.status)
				error.value = true
				return
			}
			const data1 = await resp1.json()
			moon_data.value = data1
		} catch (err) {
			console.error(err)
		} finally {
			loadingData.value = false
		}
	})

	fetch("/api/moon_data")
</script>

<template>
	<div class="error" v-if="error">
		<h1>Something went wrong. Please try again later.</h1>
	</div>
	<div class="mainView" v-else>
		<div class="dataView" v-if="!loadingData && moon_img && moon_data">
			<div>
				<img class="moonImg" :src="moon_img.imageUrl" />
			</div>
			<div class="moonData">
				<div class="card">
					<h1>Date:</h1>
					<p>{{ moon_data.date }} @ {{ moon_data.time }}</p>
				</div>
				<div class="card">
					<h1>Phase:</h1>
					<p>{{ moon_data.phase }}</p>
				</div>
				<div class="card">
					<h1>Distance:</h1>
					<p>{{ moon_data.distance }} km</p>
				</div>
				<div class="card">
					<h1>Position:</h1>
					<p>Alt: {{ moon_data.position.altitude }}</p>
					<p>Az: {{ moon_data.position.azimuth }}</p>
				</div>
			</div>
		</div>
		<div v-else><h1>Loading data, please wait...</h1></div>
		<div class="infoInput">
			<h1>Local Information</h1>
			<form>
				<input type="text" id="latitude" value="asdfasdf" required>
				<input type="text" id="longitude" value="asdfasdf" required>
				<input type="datetime-local" id="datetime" required>
			</form>
		</div>
	</div>
</template>
