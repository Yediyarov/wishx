// Comment to donation functionality in wish detail page
//#region Comment Websocket
let wish_page_url = $('#wish-page-url').val();
let wsStart = 'ws://';
let loc = window.location;
if (loc.protocol == 'https:') {
    wsStart = 'wss://'
}
let socket_url = wsStart + window.location.host + wish_page_url;
let socket = new ReconnectingWebSocket(socket_url);
socket.onmessage = function (event) {
    // console.log(event);
    let newComment = JSON.parse(event.data);
    let donation_id = newComment['donation_id'];
    let comment_text = newComment['comment_text'];
    let user_fullname = newComment['full_name'];
    let user_picture = newComment['user_picture'];
    let comment_creation_date = newComment['created_at'];
    let comment_id = newComment['comment_id'];
    let current_donation = $(`li[data-id=${donation_id}]`);

    let reply_form = current_donation.find(".donation__reply");
    let donation_mockup = $(".donation_mockup .donation__comment").clone();

    let pp = donation_mockup.find(".card__image");
    let fname = donation_mockup.find(".donation__username");
    let comment = donation_mockup.find(".event__text");
    let since_comment = donation_mockup.find('.comment-since');
    let comment_heart = donation_mockup.find('.comment_heart');
    let comment_like_count = donation_mockup.find('.comment_like_count');

    pp.attr("src", user_picture);
    fname.html(user_fullname);
    comment.html(comment_text);
    since_comment.html(comment_creation_date);
    comment_heart.attr('data-id', comment_id);
    comment_like_count.attr('data-id', comment_id);

    reply_form.find("form").trigger("reset");
    if (reply_form.length) {
        donation_mockup.insertBefore(reply_form);
    } else {
        current_donation.append(donation_mockup);
    }
};
socket.onopen = function (event) {
    // console.log('socket opened', event);
    let form = $('#reply__form');
    form.submit(function (e) {
        e.preventDefault();
        let comment_text = $('#reply-text').val();
        let user = $('#comment-user').val();
        let donation_id = $(this).closest('li').data('id');
        data = {
            'comment_text': comment_text,
            'user': user,
            'donation_id': donation_id,
        };
        // Send data to consumer
        socket.send(JSON.stringify(data))
    });
};

socket.onclose = function (event) {
    // console.log('socket closed', event)
};
//#endregion Comment Websocket

//------------------------------------------------------------------------------

//#region Like Donation Websocket
let like_dislike_url = $('#like-dislike-url').val();
let like_dislike_socket_url = wsStart + window.location.host + like_dislike_url;
let like_dislike_socket = new ReconnectingWebSocket(like_dislike_socket_url);

like_dislike_socket.onmessage = function (event) {
    // console.log('socket receive message', event);
    let like_data = JSON.parse(event.data);
    let like_type = like_data['type'];
    let like_count = like_data['like_count'];
    let item_id = like_data['item_id'];
    let current_donation = $(`li[data-id=${item_id}]`);
    if (like_type === 'donation') {
        let current_donation_like_count = current_donation.find('.donation_like_count');
        current_donation_like_count.text(like_count);
    } else if (like_type === 'comment') {
        let current_comment_count = $(`.comment_like_count[data-id="${item_id}"]`);
        current_comment_count.text(like_count);
    }
};
like_dislike_socket.onopen = function (event) {
    // console.log('socket opened', event);
    let user = $('#comment-user').val();
    // Donation like socket
    $('.donation_heart').click(function (e) {
        let current_donation = $(this);
        let donation_id = current_donation.data('id');
        let liked = 0;
        if ($("path", current_donation).hasClass('donation__heart--selected')) {
            liked = 1;
        }
        $("path", current_donation).toggleClass('donation__heart--selected');
        data = {
            'item_id': donation_id,
            'liked': liked,
            'user': user,
            'type': 'donation',
        };
        // Send data to consumer
        like_dislike_socket.send(JSON.stringify(data))
    });
    // Comment like socket
    $(document).on('click', '.comment_heart', function () {
        let current_comment = $(this);
        let comment_id = $(this).data('id');
        let liked = 0;
        if ($("path", current_comment).hasClass('donation__heart--selected')) {
            liked = 1;
        }
        $("path", current_comment).toggleClass('donation__heart--selected');
        data = {
            'item_id': comment_id,
            'liked': liked,
            'user': user,
            'type': 'comment',
        };
        // Send data to consumer
        like_dislike_socket.send(JSON.stringify(data))
    });
};
like_dislike_socket.onclose = function (event) {
    // console.log('socket closed', event)
};
//#endregion Like Donation Websocket
