function getQueryResults(){
    var query = $("#query_input").val();
    console.log(query)
    $.ajax({
        url: "http://127.0.0.1:5000/get_urls/" + query,
        success: function(result){
            $("#result_label").text(result);
        }
    })
}