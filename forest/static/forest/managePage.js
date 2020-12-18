$(document).ready(function(){
    $('#edit').click(() => {
        toggleEdit();
    });
});

function toggleEdit() {
    //Changing content of edit menu element
    if ($('#edit b').text() == "Edit pages") {
        $('#edit b').text('Stop editing');
        switchAnimation(false); //Turning on hover animation
    } else {
        $('#edit b').text('Edit pages');
        switchAnimation(true);  //Turning off hover animation
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