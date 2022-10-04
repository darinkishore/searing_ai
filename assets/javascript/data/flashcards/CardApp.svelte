<script>
	import Flashcard from './Flashcard.svelte';
	import {onMount, tick} from "svelte";
	import {ApiApi} from "../../api-client";
	import {getApiConfiguration} from "../../api";
	import {writable} from "svelte/store";

	const client = new ApiApi(getApiConfiguration(SERVER_URL_BASE));


	const vocab = writable([
		{
			"question": "Hold your horses! We're still processing.\n" +
					"Refresh the page in a few seconds, and give it another go.",
			"answer": "There's no need to rush. Go tell your mother you love her."
		}
	]);

	onMount(async () => {
		let data = client.apiDocumentsQuestionsList({'documentId': DOC_ID}).then((response) => {
		let questionList = [];
		response.results.forEach((pair) => {
		questionList.push({
					question: pair['question'],
					answer: pair['answer']
				})
	});
		$vocab = questionList;
	});
	});


	let flashcardIndex = 0;

	// wait for data to load before initializing clue and answer
	console.log($vocab);
	$: clue = $vocab[flashcardIndex].question;
	$: answer = $vocab[flashcardIndex].answer;

	let showCardBack = false;
	const toggleShowBack = () => showCardBack = !showCardBack;

	const prevCard = () => {
		showCardBack = false;
		if (flashcardIndex === 0) {
			flashcardIndex = $vocab.length-1;
		} else {
			flashcardIndex -= 1;
		}
	}

	const nextCard = () => {
		showCardBack = false;
		if (flashcardIndex === $vocab.length-1) {
			flashcardIndex = 0;
		} else {
			flashcardIndex += 1;
		}
	}
</script>

<main class="w-full">
	<!-- FLASHCARD -->
		<div class="flip-box w-full">
		<div class="flip-box-inner" class:flip-it={showCardBack}>
			<Flashcard {clue}
								 {answer}
								 {showCardBack}
								 />
		</div>
	</div>

	<!-- BUTTONS -->
	<div id="btn-cont">
		<button class="arrow-btn" on:click={prevCard}>&#8592;</button>

		<button on:click={toggleShowBack}>
			{showCardBack ? "Hide Answer" : "Show Answer"}
		</button>

		<button class="arrow-btn" on:click={nextCard}>&#8594;</button>
	</div>

</main>


<style>
	main {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin: 5%;
		height: 60vh;
	}

	/* The flip box container - set the width and height to whatever you want. We have added the border property to demonstrate that the flip itself goes out of the box on hover (remove perspective if you don't want the 3D effect */
	.flip-box {
		@apply bg-gray-100;
		aspect-ratio: 3/1.5;
/* 		border: 1px solid #ddd; */
	}

	/* This container is needed to position the front and back side */
	.flip-box-inner {
		position: relative;
		width: 100%;
		height: 100%;
		text-align: center;
		transition: transform 0.4s;
		transform-style: preserve-3d;
	}

	/* Do an horizontal flip on button click */
	.flip-it {
		transform: rotateY(180deg);
	}

	#btn-cont {
		width: 200px;
		padding: 10px 0;
		display: flex;
		justify-content: space-between;
	}

	button {
		@apply btn;
		padding: 8px 8px;

	}

	button:active {
		@apply btn-active;
	}
</style>