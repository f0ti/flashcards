$(document).ready(function() {
    // Toggle flashcard answer
    $('.toggle-answer-btn').click(function() {
        $(this).parent().find('.flashcard-answer').toggleClass('d-none');
    });

    // Toggle flashcard visibility and add animation
    $('.list-group-item').click(function() {
        $(this).find('.flashcard-answer').toggleClass('d-none');
        $(this).addClass('flashcard-clicked');
        setTimeout(() => {
            $(this).removeClass('flashcard-clicked');
        }, 500);
    });

    // Fade in flashcards on page load
    $('.list-group-item').addClass('fade-in');
});
