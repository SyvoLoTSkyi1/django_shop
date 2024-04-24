// function updateWishlist (element) {
//     let itemId = element.data('item'),
//         heart = element.find('svg.bi-heart'),
//         heartFill = element.find('svg.bi-heart-fill');
//
//
//     $.ajax({
//         url: '/ajax-wishlist/' + itemId + '/',
//         method: 'GET',
//         success: function (data) {
//             if (data.created === true) {
//                 heart.addClass('d-none');
//                 heartFill.removeClass('d-none');
//
//
//             } else {
//                 heart.removeClass('d-none');
//                 heartFill.addClass('d-none');
//
//
//             }
//         },
//         error: function(xhr, status, error) {
//             console.error(status, error);
//     }
//     });
// }
//
//
// function updateWishlistRemove (element) {
//     let itemId = element.data('item'),
//         card = element.closest('.card');
//
//
//
//     $.ajax({
//         url: '/ajax-wishlist/' + itemId + '/',
//         method: 'GET',
//         success: function (data) {
//             if (data.created === false) {
//                 card.addClass('d-none');
//                 console.log(created)
//
//
//
//             }
//         },
//         error: function(xhr, status, error) {
//             console.error(status, error);
//     }
//     });
// }


function updateWishlist (element, context) {
    let itemId = element.data('item'),
        heart = element.find('svg.bi-heart'),
        heartFill = element.find('svg.bi-heart-fill'),
        card = element.closest('.card');


    $.ajax({
        url: '/ajax-wishlist/' + itemId + '/',
        method: 'GET',
        success: function (data) {
            if (context === 'remove') {
                if (data.created === false) {
                    card.addClass('d-none');
                }
        } else {
                if (data.created === true) {
                    heart.addClass('d-none');
                    heartFill.removeClass('d-none');
                } else {
                    heart.removeClass('d-none');
                    heartFill.addClass('d-none');
                }
            }
        },
        error: function(xhr, status, error) {
            console.error(status, error);
    }
    });
}
