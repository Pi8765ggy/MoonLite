<script setup>
	// ref = reactive variables
	// onMounted = run code on load
	import { ref, onMounted } from "vue"

	const loadingData = ref(true)
	const user = ref({})

	onMounted(async () => {

		try {
			const resp = await fetch("/api/user", {
				credentials: "include"
			})
			const data = await resp1.json()
			user.value = data1
		} catch (err) {
			console.error(err)
		} finally {
			loadingData.value = false
		}

	})
	
	// Now we take them to a fancy page with router
	/*
	function login() {
		window.location.href = "/auth/login"
	}
	*/

	async function logout() {

		await fetch('/auth/logout', {
			credentials: "include" 
		})

		const res = await fetch('/api/user', {
			credentials: "include"
		})
		const dat = await res.json()

		user.value = dat
	}

</script>

<template>
  <div class="app">

    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-left">
        <div class="logo">MoonLite</div>
      </div>

      <div class="nav-right">
	<div v-if="!user.logged_in">
        	<button class="login-btn" @click="login">Login</button>
	</div>
	<div v-else>
		<img :src="user.picture" height=40px width=40px />
		<p> Hello, {{ user.name }}!</p>
		<button class="login-btn" @click="logout">Logout</button>
	</div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="content">
	    <router-view />
    </main>

  </div>
</template>

<style scoped>
</style>
