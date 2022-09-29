<script>
import {ApiApi} from "../api-client";
import {getApiConfiguration} from "../api";
import {doc_list} from "../stores";
import {onMount} from "svelte";

// has a csrf token!
let client = new ApiApi(getApiConfiguration(SERVER_URL_BASE));

</script>

<main>

<form class="max-w-lg" hx-post="/upload" enctype="multipart/form-data" id="docform">
    <div class="py-4">
        <input type="file" name="file" class="pb-4" required="" id="id_file">
        <input class="input input-bordered w-full" type="text"
               name="title" maxlength="255" placeholder="Document Title" required="" id="id_title">
    </div>

    <!-- On submit, this triggers the hx-post request. -->
    <button type="submit" class="pg-button pg-button-secondary">
        Upload</button>
</form>

</main>

