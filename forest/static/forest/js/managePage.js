$(document).ready(function(){
    //Hide container with buttons
    switchControlButtons(true);
    //Turning on or off Editing mode when button is pressed
    $('#edit').click(() => {
        toggleEdit();
    });
    //Triggering removeModal function when pressing remove button
    $('.removeButton').on('click', function() {
        removeModal($(this).data('id'));
    })
    //Triggering editModal function when pressing edit button
    $('.editButton').on('click', function() {
        editModal($(this).data('id'));
    });
});

function toggleEdit() {
    //Changing content of edit menu element
    if ($('#edit b').text() == "Edit pages") {
        $('#edit b').text('Stop editing');
        switchAnimation(false); //Turning on hover animation\
        switchControlButtons(false); //Turning on control buttons
    } else {
        $('#edit b').text('Edit pages');
        switchAnimation(true);  //Turning off hover animation
        switchControlButtons(true); //Turning off control buttons
    }
}

function switchAnimation(animation) {
    let action = animation;

    if (action) {
        console.log("switch animation on!");
        $('.page').css("animation-play-state", "running");
    } else {
        console.log("switch animation off!");
        $('.page').css("animation-play-state", "paused");
    }

}

function switchControlButtons(action) { 
    document.querySelectorAll('.control-buttons').forEach(container => {
        if (action) {
            container.style.display = "none";
        } else {
            container.style.display = "block";
        }
    });
}

function removeModal(pageID) {
    //Show confirmation modal
    $('#removePage').modal('show');
    //Passing ID value to the modal remove button
    $('#confirmRemove').val(pageID);
}


function editModal(pageID) {
    //Show edit modal
    $('#editPage').modal('show');
    //Passing ID value to the modal edit button
    $('#confirmEdit').val(pageID);
    //Isert values to the input fields on the edit modal
    getEditData(pageID);
}


function getEditData(pageID) {
    fetch(`/pageData/${pageID}`, {
        method: 'GET'
    }).then(response => response.json())
    .then(data => {
        $('#editPageInput').val(data['url']);
        $('#editTitleInput').val(data['name']);
        $('#editBGcolor').val(data['BGcolor']);
        $('#editTxtColor').val(data['TxTcolor']);
    });
}