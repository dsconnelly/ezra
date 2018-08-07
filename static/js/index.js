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
        var sel_id = dept_short + number + required[i];
        to_add += "<select id=\"" + sel_id + "\" class=\"meetingGroup\">";
        to_add += "<option value=\"\" disabled selected>select " + required[i] + "</option>";

        var available_groups = meeting_group_data[required[i]];
        for (j = 0; j < available_groups.length; j++) {
            to_add += "<option value=\"" + available_groups[j] + "\">" + available_groups[j] + "</option>";
        }

        to_add += "</select><br/>";
    }

    to_add += "<button class=\"classInfoReset\">clear</button>";

    $(this).html(to_add);
    turn_off_info_cell($(this));

    $(".meetingGroup").change(function() {
        add_block_to_schedule($(this))
    })
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

    cell.find("select").each(function() {
        var sel_id = $(this).attr("id");
        $("." + sel_id).each(function() {
            $(this).css("background-color", "#F7F7F7");
            $(this).removeClass(sel_id);
        })
    });

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

function add_block_to_schedule(select) {
    var sel_id = select.attr("id");
    $("." + sel_id).each(function() {
        $(this).css("background-color", "#F7F7F7");
        $(this).removeClass(sel_id);
    })

    var opt_parts = select.val().split(" ");
    var days = opt_parts[0];
    var start = opt_parts[1];
    var end = opt_parts[3];

    var start_split = start.split(":");
    var start_h = Number(start_split[0]);
    var start_m = Number(start_split[1]);

    var end_split = end.split(":");
    var end_h = Number(end_split[0]);
    var end_m = Number(end_split[1]);

    var start_h_row = 1 + ((start_h - 8) * 12);
    var start_m_row = start_m / 5;
    var start_row = start_h_row + start_m_row;

    var end_h_row = 1 + ((end_h - 8) * 12);
    var end_m_row = end_m / 5;
    var end_row = end_h_row + end_m_row;

    var table = $("#scheduleTable");

    for (i = 0; i < days.length; i++) {
        var d = days.charAt(i);
        var d_idx = "MTWRF".indexOf(d) + 1;

        for (j = start_row; j < end_row; j++) {
            var col = d_idx
            if (!((j - 1) % 12 == 0)) {
                col = col - 1;
            }

            cell = $("#scheduleTable tr").eq(j).find('td').eq(col);
            cell.css("background-color", "#B31B1B");
            cell.addClass(sel_id);

        }
    }
}
