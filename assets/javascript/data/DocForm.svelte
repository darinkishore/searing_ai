<script>
import {ApiApi} from "../api-client";
import {getApiConfiguration} from "../api";
import axios from 'axios';
import {doc_list} from "../stores.js";

// this is a svelte component

let client = new ApiApi(getApiConfiguration(SERVER_URL_BASE));
let doc_file;
let input;
let doc_title;


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
    console.log(values);

    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios({
        method: 'post',
        url: '/upload',
        data: values,
        headers: {'Content-Type': 'multipart/form-data'},
    })
    // wait for request to complete then poll /api/documents for paginated list
    // and push them to the store

    // TODO: clean up document fetching

    async () => {
        let documents = [];
        // docs is a temp var to hold results of call
        let docs = await client.apiDocumentsList().catch((err) => {});
        docs['results'].forEach(doc => {
            documents.push(doc);
        })
        documents.sort((a, b) => b.createdAt - a.createdAt);
        $doc_list.set(documents);
    }


    // re-render form
    doc_title = null;
    input.value = '';
}


</script>

<main>

<h1 class="pg-title mt-2 text-lg">Upload a Document!</h1>

<form class="max-w-lg" enctype="multipart/form-data" on:submit|preventDefault={handleUpload} id="docform">
    <div class="py-4">
        <input bind:value={doc_file} bind:this={input} type="file" name="file" class="pb-4" required="" id="id_file">
        <input bind:value={doc_title} class="input input-bordered w-full" type="text"
               name="title" maxlength="255" placeholder="Document Title" required="" id="id_title">
    </div>

    <!-- On submit, this triggers the hx-post request. -->
    <button type="submit" class="pg-button pg-button-secondary">
        Upload</button>
</form>

</main>

