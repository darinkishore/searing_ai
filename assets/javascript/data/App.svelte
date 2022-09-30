<script>
import {ApiApi} from "../api-client";
import {getApiConfiguration} from "../api";
import {onMount, afterUpdate, onDestroy, tick} from "svelte";
import {fade} from "svelte/transition";
import { quintInOut } from "svelte/easing";
import {doc_list} from "../stores.js";

// implement a document_list array store

let elems = [];

const client = new ApiApi(getApiConfiguration(SERVER_URL_BASE));

afterUpdate(async () => {
    let documents = [];
    // docs is a temp var to hold results of call
    let docs = await client.apiDocumentsList().catch((err) => {});
    docs['results'].forEach(doc => {
        documents.push(doc);
    })
    documents.sort((a, b) => b.createdAt - a.createdAt);
    elems = elems.filter((elem) => (elem !== null));
    $doc_list = documents;
});

function deleteDocument(id) {
    client.apiDocumentsDestroy({'id' : id}).catch((err) => {
        console.log(err);
    });
    elems = elems.filter((elem) => (elem !== null));
    doc_list.update((docs) => docs.filter((doc) => doc.id !== id));
}

</script>

<main>
<div id="doctable" class="px-2 sm:px-2 lg:px-2">
    <div class="sm:flex sm:items-center">
        <div class="sm:flex-auto">
            <h1 class="pg-title mt-2 text-lg">Your Documents:</h1>
        </div>
    </div>
    <div class="mt-4 flex flex-col">
        <div class="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div class="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
                    <table class="min-w-full divide-y divide-gray-300">
                        <!-- Table header -->
                        <thead class="bg-gray-50">
                        <tr>
                            <th id = "doc-name" scope="col"
                                class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                                <p class="group inline-flex">Name</p>
                            </th>
                            <th id="ul-date" scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                <p class="group inline-flex">Last Modified</p>
                            </th>
                            <th id="summary" scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                <p class="group inline-flex"></p>
                            </th>
                            <th id="questions" scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                <p class="group inline-flex"></p>
                            </th>
                            <th id = "download" scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">
                                <span class="sr-only"></span>
                            </th>
                        </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 bg-white">
                        <!-- Table rows -->
                        {#each $doc_list as doc, index}
                            <tr bind:this={elems[index]} transition:fade="{{duration: 400, easing:quintInOut}}" >
                                <td class="py-4 pl-4 pr-3 text-sm font-medium text-gray-900 whitespace-nowrap sm:pl-6">
                                    <a href="{doc.file}" class="text-indigo-600 font-semibold hover:link hover:text-indigo-900">{doc.title}</a>
                                </td>
                                <td class="px-3 py-4 text-sm text-gray-500 whitespace-nowrap">
                                    {doc.createdAt.getMonth()}/{doc.createdAt.getDate()}/{doc.createdAt.getFullYear()}
                                </td>
                                <td class="px-3 py-4 text-sm text-gray-500 whitespace-nowrap">
                                    <a href="doc{doc.id}/summary"
                                    class="text-indigo-600 hover:text-indigo-900" >
                                        Summary</a>
                                </td>
                                <td class="px-3 py-4 text-sm text-gray-500 whitespace-nowrap">
                                    <a href="doc{doc.id}/questions"
                                       class="text-indigo-600 hover:text-indigo-900">
                                        Questions</a>
                                </td>
                                <td hx-sync="this:drop" class="px-3 py-4 text-sm whitespace-nowrap text-right">
                                    <button on:click={() => deleteDocument(doc.id)}
                                       class="text-red-600 hover:link hover:text-red-900">
                                        Delete</button>
                                </td>
                            </tr>
                        {/each}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
</main>