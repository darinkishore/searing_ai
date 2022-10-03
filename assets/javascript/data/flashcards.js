import CardApp from './flashcards/CardApp.svelte';

const cards = new CardApp({
	target: document.getElementById("flashcards")
});

export default cards;