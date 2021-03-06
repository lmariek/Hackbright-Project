
"use strict";

function myFunction() {
  let input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("case-table");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

///////////////////////////////
// ATTNY BAR CHART FUNCTIONS //
///////////////////////////////

function createAttnyAvail() {

    let options = {
        responsive: true,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }

    let ctx_bar = $("#attnyBarChart").get(0).getContext("2d");

    // let green_red_gradient = bar_ctx.createLinearGradient(0, 0, 0, 600);
    // green_red_gradient.addColorStop(0, 'red');
    // green_red_gradient.addColorStop(1, 'green');

    $.get("/attorney_data.json", function (data) {
      let attorneyAvail = new Chart(ctx_bar, {
                                              type: 'horizontalBar',
                                              data: data,
                                              options: options
                                            });
    });

}

$("#availChart").click(function(){
    createAttnyAvail();
    $("#attnyBarChart").toggle();
    $("#progressChart").toggle();
});

//////////////////////////////////
// USER LINE GRAPH ON DASHBOARD //
//////////////////////////////////

function showUserInfo() {

    // Make Line Chart of Melon Sales over time
    let ctx_line = $("#progressChart").get(0).getContext("2d");

    let options = {
      responsive: true
    };

    $.get("/userProgress.json", function (data) {
      let myLineChart = Chart.Line(ctx_line, {
                                    data: data,
                                    options: options
                                });
    });
}

showUserInfo();

///////////////////////
// NOTEPAD FUNCTIONS //
///////////////////////

function checkWebStorageSupport() {

    if(typeof(Storage) !== "undefined") {
        return(true);
    }
    else {
        alert("Web storage unsupported!");
        return(false);
    }
}

function displaySavedNote(noteKey) {

    if(checkWebStorageSupport() === true) {
        let result = JSON.parse(localStorage.getItem(noteKey));

        if (result === null) {
        result = "No note saved";
        }

        document.getElementById('area').value = result.txt;
    }
}

function listSavedNotes(caseID) {

    if(checkWebStorageSupport() === true) {

        let noteValues = {},
        noteKeys = Object.keys(localStorage);

        for (let key of noteKeys) {
            let noteObj = JSON.parse(localStorage.getItem(key));
            if (noteObj.case_id == caseID) {
                noteValues[key] = noteObj;
            }
        }

        let trHTML = '';

        for (let key in noteValues) {
            let value = noteValues[key];
            trHTML += "<tr><td><li><a href='#' class='case-note' data-key='" + key + "'>" + value.date + "</a></li></td></tr>";
        }

        $("#display-notes").html("<b>Notes:</b>");
        $("#display-notes").append(trHTML);
    }
}

function saveNote(caseID) {

    let today = new Date();
    let todayStr = today.toDateString();
    let todayStrKey = String(today);

    if(checkWebStorageSupport() == true) {
        let noteInput = document.getElementById("area");

        if(noteInput.value != '') {

            let noteObj = {"case_id":caseID,
                           "txt": noteInput.value,
                           "date": todayStr
                          };

            let noteObjJSON = JSON.stringify(noteObj);
            localStorage.setItem(todayStrKey, noteObjJSON);
        }

        else {
            alert("Nothing to save");
        }
    }
}

function downloadNote(filename) {

    let text = document.getElementById("area");
    let pom = document.createElement('a');
    pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    pom.setAttribute('download', filename);

    if (document.createEvent) {
        let event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

function closeNote() {
    // this line clears content
    document.getElementById('area').value = "";
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#progressChart").toggle();
}


$(".new-notes").click(function(){
    document.getElementById('area').value = "";
    let caseID = $(this).data("case-id");
    $("#save-note").attr("data-case-id", caseID);
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#progressChart").toggle();
    $("#case-note-tag").html("Write a note for Case <b>" + caseID + "</b>:");
});

$("#close-note").click(function(){
    closeNote();
});


$("#save-note").click(function(){
    let caseID = $(this).data("case-id");
    saveNote(caseID);
});


$("#download-note").click(function(){
    downloadNote();
});

$(".case-row").click(function(){
    let caseID = $(this).data("case-id");
    listSavedNotes(caseID);
    $.each($(this).find(".tri-toggle"),
        function(element) {
            $(this).toggle();
        }
    );
});

$(document).on("click", ".case-note", function(){
    let noteKey = $(this).data("key");
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#progressChart").toggle();
    displaySavedNote(noteKey);
});


///////////////////
// SEARCH ENGINE //
///////////////////


function getResults() {

    let query = $("#user-lit-search").val();

    $.get("/search_results/" + query, function(data) {

        let trHTML = '';

        for (let result in data) {

            let previewText = data[result].highlights;
            let path = data[result].path;
            // let resultQuant = data.total_hits;
            // let docType = data[result].doc_type;

            // let previewText = result['highlights'];
            // trHTML += "<tr><td><b><u>" + docType + "</u></b></td></tr>";
            trHTML += "<tr><td>" + previewText + "</td></tr>";
            trHTML += "<tr><td><a href='/download/" + path + "'>Download</a></td></tr>";
        }

        // $("#search-results-div").html("<h2>Search Results:</h2>");
        $("#search-results-table").append(trHTML);

    });

    $("#search-results-table").toggle();
    $("#search-results-div").toggle();
    $("#progressChart").toggle();
    $("#caseInfo").toggle();
}

$("#user-lit-search").keyup(function(event) {
    // if person pressed enter
    if (event.which == 13) {
        getResults();
    }
    });

$("#lit-search").click(function(event) {
    getResults();
    });

$("#dash-redirect").click(function() {
    $("#search-results-table").toggle();
    $("#search-results-div").toggle();
    $("#progressChart").toggle();
    $("#caseInfo").toggle();
    document.getElementById('user-lit-search').value = "";
    });


/////////////////////
// MAKE A TIMELINE //
/////////////////////

function showCaseHistory(buttonID) {

    $.get("/casehistory.json", function (data) {
        $('#complaint-info').html(data[buttonID]['complaint']);
        $('#answer-info').html(data[buttonID]['answer']);
        $('#interrogatories-info').html(data[buttonID]['interrogatories']);
        $('#requestprodocs-info').html(data[buttonID]['request_pro_docs']);
    });
}

$(".show-timeline").click(function(){
    $("#timeline").toggle();
    $("#progressChart").toggle();
    let buttonID = $(this).attr("id");
    showCaseHistory(buttonID);
});


////////////////////
// BOUNDING BOXES //
////////////////////

$("#bounding-box-btn").click(function(){
    $("#caseInfo").toggle();
    $("#progressChart").toggle();
});



