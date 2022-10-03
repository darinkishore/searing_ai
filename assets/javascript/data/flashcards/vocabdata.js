import {ApiApi} from "../../api-client";
import {getApiConfiguration} from "../../api";


let client = new ApiApi(getApiConfiguration(SERVER_URL_BASE));
// on page load


export const vocab = await getVocab();

export const bocab = [
	{
		answer: "Christmas tree",
		question: "who?"
	},
	{
		answer: "reindeer",
		question: "what?"
	},
	{
		answer: "wreath",
		question: "when?"
	},
];

// create async function to get data from API

export async function getVocab() {
	let data = await client.apiDocumentsQuestionsList({'documentId': DOC_ID})
	let questionAnswerPairs = data['results'];
	questionAnswerPairs.forEach((pair) => {
		vocab.push(
			{
				question: pair['question'],
				answer: pair['answer']
			}
		)
	});
}