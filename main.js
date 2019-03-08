function getQueryResults(){
    var query = $("#query_input").val();
    console.log(query)
    $.ajax({
        url: "http://127.0.0.1:5000/get_urls/" + query,
        success: function(result){
            $("#result_label").empty()
            if (result.length == 0){
                $("#result_label").append("much empty")
            }
            for (let i = 0; i < result.length; i++){
                let count = i+1;
                console.log(result[i])
                $("#result_label").append(count+": <a href=http://" + result[i] + ">" + result[i] + "</a><br/>");
            }
        }
    })
}