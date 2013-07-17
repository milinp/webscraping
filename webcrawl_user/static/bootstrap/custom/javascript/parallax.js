function EasyPeasyParallax() {
    scrollPos = $(this).scrollTop();
    $('#banner').css({
        'background-position' : '50% ' + (-scrollPos/4)+"px"
    });
    $('#bannertext').css({
        'margin-top': (scrollPos/4)+"px",
        'opacity': 1-(scrollPos/250),
    });

    var textOpacity = $('#bannertext').css('opacity');

    if (textOpacity == 0) {
        $('#bannertext').css('visibility','hidden');
    }
    else{
        $('#bannertext').css('visibility','visible');

    }

}

$(document).ready(function(){
    $(window).scroll(function() {
        EasyPeasyParallax();
    });

    $('#bannertext').hover(
    function(){
        $(this).toggleClass('shadow');
    });

    $("#bannertext").click(function (){
            $('html, body').animate({
                scrollTop: $("#content").offset().top
            }, 1000, 'swing');
    });




});