<script>
import {ApiApi} from "../../api-client";
import {getApiConfiguration} from "../../api";
import axios from 'axios';
import {fade} from "svelte/transition";
import { quintInOut } from "svelte/easing";
import {doc_list} from "../../stores.js";
import {createEventDispatcher} from 'svelte';
import {CheckCircle, Icon, X} from "svelte-hero-icons";
// this is a svelte component

let client = new ApiApi(getApiConfiguration(SERVER_URL_BASE));
let doc_file, input, doc_title;

let uploading = false;
function makeFalse() {uploading = false;}
function makeTrue() {uploading = true;}


const dispatch = createEventDispatcher();

function docsUpdated() {
    dispatch('docsUpdated');
}
docsUpdated();


function isFormValid(file, title) {
    // if data is valid return null
    // else return error message
    if (file == null)
        return 'Please select a file';

    if (title == null || title.length === 0)
        return 'Please enter a title';

    if (title.length > 255)
        return 'Title is too long';

    if (file.size > 5242880)
        return 'File is too large. Max size is 5MB.';
    return null;
}


function handleUpload() {
    let error = isFormValid(doc_file, doc_title);
    if (error != null) {
        // show error message
        alert(error);
        return;
    }

    let values = htmx.values(htmx.find('#docform'));
    makeTrue();

    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios({
        method: 'post',
        url: '/upload',
        data: values,
        headers: {'Content-Type': 'multipart/form-data'},
    })

    docsUpdated();
    setTimeout(makeFalse, 15000);

    // re-render form
    doc_title = null;
    input.value = '';
}


</script>

<main>
    {#if uploading===true}
    <div transition:fade={{duration: 400, easing:quintInOut}}
         class="grid rounded-md bg-green-50 p-1">
      <div class="flex items-center">
        <div class="flex-shrink-0 pl-4">
          <Icon src={CheckCircle} solid class=" items-center h-6 w-6 text-green-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true" />
        </div>
        <div class="ml-4">
          <p class="text-sm font-medium text-green-800">Nice! It's uploading.</p>
        </div>
        <div class="ml-auto pl-3">
          <div class="-mx-1.5 -my-1.5">
            <button type="button" on:click={makeFalse} class="inline-flex bg-green-50 rounded-md p-1.5 text-green-500 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-green-50 focus:ring-green-600">
              <span class="sr-only">Dismiss</span>
              <Icon src="{X}" solid class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </div>

    {:else if uploading===false}
    <h1 class="pg-title mt-2 text-lg" on:message >Upload a Document!</h1>
    {/if}

<form class="max-w-lg" enctype="multipart/form-data" on:submit|preventDefault={handleUpload} id="docform">
    <div class="py-4">
        <input bind:value={doc_file} bind:this={input} type="file" name="file" class="pb-4" required="" id="id_file">
        <input bind:value={doc_title} class="input input-bordered w-full" type="text"
               name="title" maxlength="255" placeholder="Document Title" required="" id="id_title">
    </div>

    <button type="submit" class="pg-button pg-button-secondary">
        Upload</button>
</form>

</main>

