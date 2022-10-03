import DocForm from './form/DocForm.svelte';
import 'htmx.org';

window.htmx = require('htmx.org');

const docForm = new DocForm({
	target: document.getElementById("svelte-form")
});

export default docForm;