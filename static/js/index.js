$( document ).ready(function() {
    $(".classInfoCell").each(function() {
        turn_on_info_cell($(this));
    });
});

function class_info_cell_add(data) {
    var dept_short = data['dept_short'];
    var number = data['number'];
    var title = data['title'];
    var required = data['required']
    var meeting_group_data = data['meeting_group_data']

    to_add = (dept_short + " " + number + ": " + title).toLowerCase() + "<br>";
    for (i = 0; i < required.length; i++) {
        to_add += "<select>";
        to_add += "<option value=\"\" disabled selected>select " + required[i] + "</option>";

        var available_groups = meeting_group_data[required[i]];
        for (j = 0; j < available_groups.length; j++) {
            to_add += "<option value=\"\">" + available_groups[j] + "</option>";
        }

        to_add += "</select><br/>";
    }

    to_add += "<button class=\"classInfoReset\">clear</button>";

    $(this).html(to_add);
    turn_off_info_cell($(this));
}

function turn_off_info_cell(cell) {
    cell.removeClass("classInfoCell");
    cell.addClass("classInfoCellFixed");

    cell.attr("contenteditable", "false");
    cell.off();

    $(".classInfoReset").click(function() {
        turn_on_info_cell($(this).parent());
    })
}

function turn_on_info_cell(cell) {
    cell.removeClass("classInfoCellFixed");
    cell.addClass("classInfoCell");

    cell.attr("contenteditable", "true");
    cell.html("click to add a class");

    cell.mousedown(function() {
        if (!(cell.is(":focus"))) {
            cell.html("");
        }
    });

    cell.keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
            cell.blur();

            var user_query = cell.html().split(" ");
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
                context: cell,
                success : class_info_cell_add,
                error : function() {
                    cell.html("class not found");
                }
            });
        }
    });
}
