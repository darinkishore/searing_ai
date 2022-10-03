<script>
	export let clue;
	export let answer;
	export let showCardBack;
</script>


<div class="flip-box-front">
	<h2>{clue}</h2>
</div>

<div class="flip-box-back" class:conceal-answer={showCardBack}>
	<h2>{answer}</h2>
</div>


<style>
	/* Position the front and back side */
	.flip-box-front, .flip-box-back {
		position: absolute;
		width: 100%;
		height: 100%;
		-webkit-backface-visibility: hidden; /* Safari */
		backface-visibility: hidden;
		box-shadow: -1px 1px 3px gray;
	}

	/* Style the front side */
	.flip-box-front {
		display: flex;
		justify-content: center;
		align-items: center;
		@apply bg-gray-50;
 		color: black;
		font-size: 1.3rem;
	}

	@keyframes revealTextSlowly {
		to { color: black }
	}

	.conceal-answer {
		animation: revealTextSlowly .3s forwards;
	}

	/* Style the back side */
	.flip-box-back {
		display: flex;
		justify-content: center;
		align-items: center;
		@apply bg-gray-50;
 		color: white;
		font-size: 1.3rem;
		transform: rotateY(180deg);
	}


</style>