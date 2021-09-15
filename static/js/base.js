/******************************************************* SITEWIDE */
/* Activate toasts (from Bootstrap) */
$(document).ready(function() {
    $(".toast").toast('show');
});

/******************************************************* INDEX.HTML */
/* Activate tooltip (from Bootstrap) */
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})


/******************************************************* ARTICLES.HTML */
/* Sort selector */
/* When selector used (change), trigger function */
$('#sort-selector').change(function() {
    /* Define selector */
    var selector = $(this);
    /* Define new URL object to allow change of 'get' parameters*/
    var currentUrl = new URL(window.location);

    /* Get the value from the selector */
    var selectedVal = selector.val();
    /* If something is selected */
    if(selectedVal != "reset"){
        /* Get sort (text before underscore) */
        var sort = selectedVal.split("_")[0];
        /* Get direction (text after underscore) */
        var direction = selectedVal.split("_")[1];
        /* Set search parameters based on obtained values */

        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);
        /* Load the updated currentURL with new parameters */

        window.location.replace(currentUrl);
    /* If nothing is selected */
    } else {
        /* Delete search parameters */
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        /* Load the updated currentURL */
        window.location.replace(currentUrl);
    }
})

/* Proposals toggle button */
/* When button toggled, submit form */
$("#proposals-form").change(function(){
    $("#proposals-form").submit();
    /* Change value to true to show user checked */
    document.getElementById("#proposals").checked = true;
});

