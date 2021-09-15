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
$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);
    var selectedVal = selector.val();
    if(selectedVal != "reset"){
        var sort = selectedVal.split("_")[0];
        var direction = selectedVal.split("_")[1];
        
        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);
        
        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");
        
        window.location.replace(currentUrl);
    }
})

/* Proposals toggle button */
$("#proposals-form").change(function(){
    $("#proposals-form").submit();
    document.getElementById("#proposals").checked = true;
});

