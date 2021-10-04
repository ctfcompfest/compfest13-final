const CORS_PROXY = "https://cf13-corsanywhere.herokuapp.com/"

function failedPromotion() {
    $(".badge-danger").show();
}

function successPromotion() {
    $(".badge-success").show();
}

function promoteWeb(link, rss) {
    let data = {
        link: link,
        rss: rss
    }

    $.ajax({
        method: "POST",
        url: "/promote",
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: successPromotion,
        error: failedPromotion
    })
}

$("form").submit(function(e) {
    e.preventDefault()
    $(".badge").hide();
    let link = $("input[name='link']").val()
    
    $.ajax({
        header: {
            origin: window.location.origin,
            "X-Requested-With": "XMLHttpRequest"
        },
        url: CORS_PROXY + link,
        success: function(data, textStatus, jqXHR) {
            promoteWeb(link, jqXHR.responseText)
        },
        error: failedPromotion
    })
})