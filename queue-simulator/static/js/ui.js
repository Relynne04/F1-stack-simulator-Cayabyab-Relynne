// Optional interface help only. Python performs every queue operation.
if (window.jQuery) {
    jQuery(function ($) {
        $('#q_data').trigger('focus');
        // After Peek, Flask marks the front item with the "peek" class. Pulse it.
        $('.stack-item.peek').hide().fadeIn(300).fadeOut(200).fadeIn(300);
    });
}
