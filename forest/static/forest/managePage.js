$(document).ready(function(){
    //Hide container with buttons
    switchControlButtons(true);
    $('#edit').click(() => {
        toggleEdit();
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