function getQueryResults(){
    var query = $("#query_input").val();
    console.log(query)
    $.ajax({
        url: "http://127.0.0.1:5000/get_urls/" + query,
        success: function(result){
            $("#result_label").empty()
            let placeholder = result.length == 0 ? "much empty" : "wow so meny results"
            $("#result_label").append(placeholder)
            for (let i = 0; i < result.length; i++){
                let count = i+1;
                console.log(result[i])
                $("#result_label").append("<br/>"+count+": <a href=http://" + result[i] + " target=_blank>" + result[i] + "</a>");
            }
        }
    })
}