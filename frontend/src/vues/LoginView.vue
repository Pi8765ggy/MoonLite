<script setup>
	function login() {
		window.location.href = "/auth/login"
	}
</script>

<template>

<div class="container">
	<div class="loginBox">
		<h1>Login</h1>
		<button @click="login">Sign in with Google</button>
	</div>
</div>

</template>

<style scoped>

.container {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 70vh;
	margin: 15px;
}

.loginBox {
	width: 30%;
	height: 75%;
	background-color: #111111;
	border-radius: 10px;
	text-align: center;
}

.loginBox h1 {
	font-size: 60px;
}

.loginBox button {
	background-color: #D3D3D3;
	border: none;
	outline: none;
	margin: 20px;
	width: 50%;
	height: 70px;
	transition: transform 0.3s;
	border-radius: 10px;
	font-weight: bold;
	font-size: 20px;
}

.loginBox button:hover {
	transform: scale(1.1);
	cursor: pointer;
}

</style>
