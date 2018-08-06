$( document ).ready(function() {
    $(".classInfoCell").mousedown(function() {
        if (!($(this).is(":focus"))) {
            $(this).html("");
        }
    });

    $(".classInfoCell").keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
            $(this).blur();

            var user_query = $(this).html().split(" ");
            var dept_short = user_query[0];
            var number = user_query[1];

            $.ajax({
                url : "/search",
                type : "POST",
                data : JSON.stringify({
                    "dept_short" : dept_short,
                    "number" : number
                }),
                dataType : "json",
                contentType: "application/json",
                context: this,
                success : function(data) {
                    this.innerHTML = data["dept_short"] + " " + data["number"] + " " + data["title"];
                },
                error : function() {
                    this.innerHTML = "class not found";
                }
            });
        }
    });
});
