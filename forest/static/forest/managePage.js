$(document).ready(function(){
    //TODO
});

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