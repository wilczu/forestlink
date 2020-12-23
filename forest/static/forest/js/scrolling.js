$('document').ready(() => {

    let navbar = [
        ['page1', 'about'],
        ['page2', 'features'],
        ['page3', 'start'],
        ['footerTop', 'top']
    ];

    $('a').click(() => {
        navbar.forEach(element => {
            $('.' + element[0]).click(() => {
                $('body, html').animate({
                    scrollTop: ($('#' + element[1]).offset().top)
                },10);
            });
        });
    });

});