// Optional interface help only. No JavaScript stack or click handlers:
// Python performs every stack operation.
if (window.jQuery) {
    jQuery(function ($) {
        $('#st_data').trigger('focus');
        // After Peek, Flask marks the top item with the "peek" class. Pulse it.
        $('.stack-item.peek').hide().fadeIn(300).fadeOut(200).fadeIn(300);
    });
}
