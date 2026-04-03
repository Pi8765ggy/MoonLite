<script setup>
	import { ref, onMounted } from "vue"
	
	// moon_img only contains the img url
	// moon_data contains the rest of the important info
	const moon_img = ref({})
	const moon_data = ref({})
	const loadingData = ref(true)
	const error = ref(false)

	const latitude = ref(null)
	const longitude = ref(null)
	const datetime = ref("")

	onMounted(async () => {
		try {	
			
			const params = new URLSearchParams({
				lat: null,
				lon: null,
				dt: null
			})

			const resp = await fetch(`/api/moon_img?${params.toString()}`)
			const resp1 = await fetch(`/api/moon_data?${params.toString()}`)
			if (!resp.ok || !resp1.ok) {
				// Catches a bad response code from the flask api
				console.error(resp.status)
				error.value = true
				return
			}
			const data = await resp.json()
			const data1 = await resp1.json()
			moon_img.value = data
			moon_data.value = data1

		} catch (err) {
			console.error(err)
		} finally {
			loadingData.value = false
		}
	})
	
	// cool syntax
	// var handleSubmit is = a function () that runs => following code {}:
	const handleSubmit = async () => {
		if (
		latitude.value === null || isNaN(latitude.value) || latitude.value > 90 || latitude.value < -90 ||
		longitude.value === null || isNaN(longitude.value) || longitude.value > 180 || longitude.value < -180
		)
		{
			error.value = true
			return
		}
		
		const params = new URLSearchParams({
			lat: latitude.value,
			lon: longitude.value,
			dt: datetime.value
		})

		try {
			loadingData.value = true

			const resp = await fetch(`/api/moon_data?${params.toString()}`)
			const resp1 = await fetch(`/api/moon_img?${params.toString()}`)
			if (!resp.ok || !resp1.ok) {
				console.error(resp.status)
				error.value = true
				return
			}
			const data = await resp.json()
			const data1 = await resp1.json()
			moon_data.value = data
			moon_img.value = data1

		} catch (err) {
			console.log(err)
		} finally {
			loadingData.value = false
		}
	}

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
			<form @submit.prevent="handleSubmit">
				<label for="latitude">Enter latitude:</label>
				<input type="number" id="latitude" :placeholder="moon_data.location.latitude" 
				min="-90" max="90" step="any" v-model.number="latitude" required>

				<label for="longitude">Enter longitude:</label>
				<input type="number" id="longitude" :placeholder="moon_data.location.longitude" 
				min="-180" max="180" step="any" v-model.number="longitude" required>

				<label for="datetime">Enter date:</label>
				<input type="datetime-local" id="datetime" v-model="datetime" required>

				<button type="submit">Submit</button>
			</form>
		</div>
	</div>
</template>
