function show_snackbar(text) {
    // Get the snackbar DIV
    let x = document.getElementById("snackbar");
    // set snackbar text
    x.innerHTML = text;
    // Add the "show" class to DIV
    x.className = "show-snackbar";
    // After 5 seconds, remove the show class from DIV
    setTimeout(function () {
        x.className = x.className.replace("show", "");
    }, 3000);
}

function showSelectedFilesCount(current_input, message_block) {
    let current_lang = window.location.pathname.split('/')[1];
    let current_file_input = $(`#${current_input}`);
    if (current_lang === 'az') {
        $(`#${message_block}`).text(current_file_input[0].files.length + ' şəkil seçilib');
    } else if (current_lang === 'en') {
        $(`#${message_block}`).text(current_file_input[0].files.length + ' photos selected');
    } else if (current_lang === 'ru') {
        $(`#${message_block}`).text('Выбрано ' + current_file_input[0].files.length + ' фотографии');
    }
};
$(document).ready(function () {
    //Load more functionality in wish list page
    //#region Load more
    $('#load_more').click(function () {
        let current_page = Number($(this).data('id'));
        let next_page = (current_page + 1).toString();
        const request_url = $('#request-url').val();
        const wishes_container = $('#wishes-container');
        const current_url = $('#current-url').val();
        $(this).data('id', next_page);
        $.ajax({
            url: request_url,
            type: "GET",
            data: {'page': next_page},
            success: function (data) {
                $(data).css('display', 'none').appendTo(wishes_container).slideDown();
                $.ajax({
                    url: current_url,
                    type: 'GET',
                    data: {'page': next_page},
                    success: function (data) {
                        //    load more button remove here
                        let all_wishes_count = $('#all_wishes_count').val();
                        let displayed_wishes_count = ($('.wish-list-card').length).toString();
                        if (all_wishes_count === displayed_wishes_count) {
                            $('#load_more').remove();
                        }
                    },
                    error: function (xhr, errmsg, err) {
                        console.log(xhr, errmsg, err);
                    }
                });
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr, errmsg, err);
            } // end error: function
        });
    });
    //#endregion

    // Delete wish functionality in user detail page
    //#region Delete wish
    $('.delete-event').click(function () {
        let wish = $(this).closest('.wish-card');
        let slug = $(this).data('slug');
        let deletion_form = $('#delete-form');
        const deletion_url = $('#wish-delete-url').val();
        const deletion_modal = $('#wish-delete-modal');
        deletion_form.on('submit', function (e) {
            e.preventDefault();
            $.ajax({
                url: deletion_url,
                type: 'GET',
                data: {'slug': slug},
                success: function (data) {
                    deletion_modal.removeClass('wishx-modal--active');
                    wish.remove();
                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr, errmsg, err);
                }
            });
        })
    });
    //#endregion Delete wish

    // Footer subscribe form
    //#region Subscribe
    $('.subscribe__form').each(function () {
        $(this).submit(function (e) {
            let base_form = $(this);
            let data = $(this).serialize();
            let url = $(this).data('action');
            e.preventDefault();
            $.ajax({
                url: url,
                type: "POST",
                data: data,
                success: function (data) {
                    if (data.save) {
                        // base_form.find("input[type=text], input[type=email], textarea").val("");
                        base_form[0].reset();
                        show_snackbar("Successfully subscribed");
                    } else {
                        show_snackbar(data.message.email[0]);
                    }
                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr, errmsg, err);
                } // end error: function
            });

            return false;
        });
    });
    //#endregion Subscribe

    //#region select files on create wish
    $('#event-photo-input').change(function (e) {
        showSelectedFilesCount('event-photo-input', 'selected_img_count');
    });
    $('#identification-card-input').change(function (e) {
        $('#file-error-text').empty();
        showSelectedFilesCount('identification-card-input', 'identification_card_img_count');
    });
    //#endregion select files on create wish
});