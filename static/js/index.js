$( document ).ready(function() {
    $(".courseInputCell").each(function() {
        turn_on_input_cell($(this));
    });
});

function turn_on_input_cell(cell) {
    // There are two classes these cells may have. They all begin with class
    // courseInputCell. In this state they may be used for inputting searches.
    // Alternatively, they may have class courseInfoCell. In this state a course
    // has already been selected, and section information is being displayed.
    cell.removeClass('courseInfoCell');
    cell.addClass('courseInputCell');

    // Now we check if there was a course in this cell before, and if there was,
    // we unshade all the calendar boxes that might have been  there.
    cell.find("select").each(function() {
        var s_id = $(this).attr("id");
        $("." + s_id).each(function() {
            $(this).css("background-color", "#F7F7F7");
            $(this).removeClass(s_id);
        });
    });

    cell.attr("contenteditable", "true");
    cell.html("click to add a class");

    // We set text in the cell to disappear when the cell is clicked. But we use
    // mousedown instead of click, since click sets the focus and then our check
    // for focus would always be vacuously true. We need to check for focus so
    // that the text only is deleted if the user wasn't previously typing in
    // this cell.
    cell.mousedown(function() {
        if (!(cell.is(":focus"))) {
            cell.html("");
        }
    });

    // Now we wait for Enter to be pushed in the cell, which triggers the call
    // to the server via AJAX.
    cell.keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
            cell.blur();

            // We make the call to the server. Eventually, we will have code
            // there  to catch the request and figure out exactly what form
            // the request is in. For this reason, we just send the whole
            // entry and let the server parse it.
            $.ajax({
                url : "/search",
                type : "POST",
                data : JSON.stringify({
                    "search" : cell.html()
                }),
                dataType : "json",
                contentType: "application/json",
                context: cell,
                success : receive_server_response,
                error : function() {
                    cell.html("server error");
                }
            });
        }
    });
}

function turn_off_input_cell(cell) {
    cell.removeClass('courseInputCell');
    cell.addClass('courseInfoCell');

    // Remove the capability to edit the cell, and remove the previously defined
    // behavior triggered by clicks.
    cell.attr("contenteditable", "false");
    cell.off();

    // Set the dropdown menus in this class to have the appropriate behavior.
    cell.find(".sectionSelect").change(function() {
        display_section($(this));
    });

    // Set the reset button to the appropriate function.
    cell.find(".courseClear").click(function() {
        turn_on_input_cell($(this).parent());
    });
}

function receive_server_response(data) {
    // We unpack some of the data for convenience later.
    var dept_short = data["dept_short"];
    var number = data["number"];
    var title = data["title"];
    var required = data["required"];
    var sections = data["sections"];

    // We store the data in sessionStorage. Potentially will use localStorage,
    // but for debugging sessionStorage makes more sense as we will want a clean
    // state each time we refresh.
    var c_id = dept_short + number; // course id
    sessionStorage.setItem(c_id, JSON.stringify(data));

    // We begin setting up the text to add to the cell.
    var to_add = ((dept_short + " " + number + ": "
        + title).toLowerCase() + "</br>");

    // For each category of required section, we add a dropdown menu.
    for (i = 0; i < required.length; i++) {
        s_id = c_id + "_" + required[i]; // select id
        to_add += "<select id=\"" + s_id + "\" class=\"sectionSelect\">";
        to_add += ("<option value=\"\" disabled selected>select "
            + required[i] + "</option>");

        for (j = 0; j < sections.length; j++) {
            // We look through all the available sections. If they are of the
            // right kind, we add an option to the dropdown and set its value
            // to be its index in the list of sections.
            if (sections[j]['kind'] == required[i]) {
                to_add += ("<option value=\"" + j.toString() + "\">"
                    + sections[j]['ref'] + "</option>");
            }
        }
        to_add += "</select></br>";
    }

    // We add the clear button.
    to_add += "<button class=\"courseClear\">clear</button>";

    // Finally, we set the cell HTML to the string we've created and call the
    // function to turn off input for this cell.
    $(this).html(to_add);
    turn_off_input_cell($(this));
}

function display_section(select) {
    // Get the id of the particular dropdown menu.
    var s_id = select.attr("id");

    // If any gridboxes were already filled in from this section, clear them.
    $("." + s_id).each(function() {
        $(this).css("background-color", "#F7F7F7");
        $(this).removeClass(s_id);
    });

    // Retrieve the section information from storage.
    var key = s_id.split("_")[0];
    var j = Number(select.val());
    var section = JSON.parse(sessionStorage.getItem(key))["sections"][j];

    var day_idxs = section["day_idxs"];
    var start_row = section["start_row"];
    var end_row = section["end_row"];

    // Get the table containing the schedule display.
    var table = $("#scheduleTable");

    // Now, we find all the five-minute cells in the appropriate ranges on
    // each day. We have to make adjustments for times exactly on the hour
    // because of the way rowspan works. However, we do not actually do the
    // coloring yet; rather, we add a class that we will use later, because
    // we will first need to make sure it does not conflict.
    for (i = 0; i < day_idxs.length; i++) {
        for (row = start_row; row < end_row; row++) {
            // Get the column to use, checking for the rowspan issue.
            var col = ((row - 1) % 12 == 0) ? day_idxs[i] : day_idxs[i] - 1;

            // Get the table cell and color it.
            cell = $("#scheduleTable tr").eq(row).find("td").eq(col);
            cell.addClass(s_id);
        }
    }

    // We check all the cells we just found. If any are already part of another
    // section, we set a flag.
    var conflict = false;
    $("." + s_id).each(function() {
        if ($(this).prop("classList").length > 2) {
            conflict = true;
        }
    });

    // If there is a conflict, we (for now) raise an alert about it and remove
    // the added class. Otherwise, we get the appropriate color and use it to
    // color in the cells we've found.
    if (conflict) {
        $("." + s_id).each(function() {
            $(this).removeClass(s_id);
        });
        alert("Cannot add this section due to a conflict");
    } else {
        var fill_color = select.parent().css("background-color");
        $("." + s_id).each(function() {
            $(this).css("background-color", fill_color);
        });
    }
}
