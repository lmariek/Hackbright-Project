
/////////////////////////
// HOMEPAGE FADE IMAGE //
/////////////////////////

$('#home-img').hover(function(){
    $('#darkness').fadeTo(100, 1);
}, function(){
    $('#darkness').fadeTo(100, 0, function(){
        $(this).show();
        $('#login-route').show();
    });
});

// $('#home-img').hover(function(){
//     $('#home-img').fadeTo(200, 0.1);
// }, function(){
//     $('#home-img').fadeTo(200, 1, function(){
//         $(this).show();
//     });
// });

// below makes both image and screen dark
// $('#home-img').hover(function(){
//     $('#darkness').fadeTo(200, 1);
// }, function(){
//     $('#darkness').fadeTo(200, 0, function(){
//         $(this).show();
//         $('#login-route').show();
//     });
// });

// $('#home-img').hover(function(){
//     $('#home-img').fadeTo(200, 0.1);
// }, function(){
//     $('#home-img').fadeTo(200, 1, function(){
//         $(this).show();
//     });
// });