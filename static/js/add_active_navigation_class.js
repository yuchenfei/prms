jQuery(function ($) {
    var path = window.location.pathname;
    $('ul a').each(function () {
        if (this.pathname === path) {
            console.log(this.pathname);
            $(this).parent().addClass('active');
        }
    });
});