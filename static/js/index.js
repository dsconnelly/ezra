$( document ).ready(function () {
    $(".classInfoCell").click(function() {
        var dept_short = prompt("Enter the department abbreviation:");
        var number = prompt("Enter the course number:");

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
    });
});
