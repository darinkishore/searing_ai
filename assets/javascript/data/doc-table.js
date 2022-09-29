import App from './App.svelte';
import {ApiApi} from "../api-client";
import {getApiConfiguration} from "../api";


const app = new App({
	target: document.getElementById("svelte-table")
});

export default app;