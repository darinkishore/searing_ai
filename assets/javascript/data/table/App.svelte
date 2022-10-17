<script>
    import {ApiApi} from "../../api-client";
    import {getApiConfiguration} from "../../api";
    import {onMount, afterUpdate, createEventDispatcher} from "svelte";
    import {fade} from "svelte/transition";
    import {quintInOut} from "svelte/easing";
    import {doc_list} from "../../stores.js";
    import {formatDistanceToNow} from 'date-fns'
    import OutClick from 'svelte-outclick';


    import DocForm from "../form/DocForm.svelte";


    let elems = [];
    const dispatch = createEventDispatcher();

    function docsUpdated() {
        dispatch('docsUpdated');
    }

    function handleUpdate(event) {
        docsUpdated();
    }

    let showModal = false;
    let doc_id = null;

    const client = new ApiApi(getApiConfiguration(SERVER_URL_BASE));

    // TODO: change so it only updates when doc_list changes
    // possibly by changing so doc_list is a child of this component
    // and then updating when event dispatched with list changed

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
        client.apiDocumentsDestroy({'id': id}).catch((err) => {
            console.log(err);
        });
        elems = elems.filter((elem) => (elem !== null));
        doc_list.update((docs) => docs.filter((doc) => doc.id !== id));
        if (showModal) {
            confirmDelete();
        }
    }

    function confirmDelete(id = null) {
        showModal = !showModal;
        doc_id = id;
    }

</script>

<main>

    {#if showModal}
        <div class="fixed z-10 inset-0 overflow-y-auto" id="delete-modal" aria-labelledby="modal-title" role="dialog"
             aria-modal="true">
            <div class="z-0 flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
                 transition:fade="{{duration: 200, easing:quintInOut}}">
                <div class="fixed inset-0 z-50 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                <!-- This element is to trick the browser into centering the modal contents. -->
                <span class="hidden z-50 sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div class=" z-50 relative inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl
     transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6"
                     transition:fade="{{duration: 200, easing:quintInOut}}">
                    <OutClick on:outclick={() => confirmDelete()}>
                        <div class="sm:flex sm:items-start">
                            <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                                <!-- Heroicon name: outline/exclamation -->
                                <svg class="h-6 w-6 text-error/90" xmlns="http://www.w3.org/2000/svg" fill="none"
                                     viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                                </svg>
                            </div>
                            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">Delete
                                    Document</h3>
                                <div class="mt-2">
                                    <p class="text-sm text-gray-500">Are you sure you want to delete this document?</p>
                                </div>
                            </div>
                        </div>
                        <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
                            <button type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-error/90 text-base font-medium text-white
         hover:bg-error focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-error sm:ml-3 sm:w-auto sm:text-sm"
                                    on:click={() => deleteDocument(doc_id)}>Delete
                            </button>
                            <button on:click={() => confirmDelete()} type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-primary
         hover:text-primary/75 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-focus sm:mt-0 sm:w-auto sm:text-sm">
                                Cancel
                            </button>
                        </div>
                    </OutClick>

                </div>
            </div>
        </div>
    {/if}


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
                        <thead >
                        <tr class="bg-base-300">
                            <th id = "doc-name" scope="col"
                                class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-base-content sm:pl-6">
                                <p class="group inline-flex">Name</p>
                            </th>
                            <th id="ul-date" scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-base-content">
                                <p class="group inline-flex">Uploaded</p>
                            </th>
                            <th id="summary" scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-base-content">
                                <p class="group inline-flex"></p>
                            </th>
                            <th id="questions" scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-base-content">
                                <p class="group inline-flex"></p>
                            </th>
                            <th id = "delete" scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">
                                <span class="sr-only"></span>
                            </th>
                        </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 bg-base-100">
                        <!-- Table rows -->
                        {#if $doc_list.length === 0}
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-base-content">
                                    <div class="flex items-center">
                                        <div class="ml-4">
                                            <div class="text-sm font-medium text-base-content">
                                                No documents uploaded. Let's get started!
                                            </div>
                                        </div>
                                    </div>
                                </td>
                        {/if}
                        {#each $doc_list as doc, index}
                            <tr bind:this={elems[index]} transition:fade="{{duration: 400, easing:quintInOut}}" >
                                <td class="py-4 pl-4 pr-3 text-sm font-medium text-gray-900 whitespace-nowrap sm:pl-6">
                                    <a href="{doc.file}" class="text-indigo-600 font-semibold hover:link hover:text-indigo-900">{doc.title}</a>
                                </td>
                                <td class="px-3 py-4 text-sm text-base-content/50 whitespace-nowrap">
                                    {formatDistanceToNow(new Date(doc.createdAt))} ago
                                </td>
                                <td class="px-3 py-4 text-sm text-base-content whitespace-nowrap">
                                    <a href="doc{doc.id}/summary"
                                    class="text-indigo-600 hover:text-indigo-900 hover:link" >
                                        Summary</a>
                                </td>
                                <td class="px-3 py-4 text-sm text-base-content whitespace-nowrap">
                                    <a href="doc{doc.id}/questions"
                                       class="text-indigo-600 hover:text-indigo-900 hover:link">
                                        Questions</a>
                                </td>
                                <td hx-sync="this:drop" class="px-3 py-4 text-sm whitespace-nowrap text-right">
                                    <button on:click={confirmDelete(doc.id)}
                                            class="text-error/60 hover:link hover:text-error">
                                        Delete
                                    </button>
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