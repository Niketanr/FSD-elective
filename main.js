$(document).ready(function() {
    // Smooth scrolling for navigation links
    $('a.nav-link').on('click', function(event) {
        if (this.hash !== "") {
            var hash = this.hash;
            var path = window.location.pathname;
            
            // Only scroll if we are on the index page
            if(path === '/' || path === '/index'){
                event.preventDefault();
                $('html, body').animate({
                    scrollTop: $(hash).offset().top - 70 // 70px offset for fixed navbar
                }, 800);
            }
        }
    });

    // Handle Service click descriptions
    $('.service-card').on('click', function() {
        // Hide all other descriptions in the same container or generally
        $('.service-desc-box').slideUp();
        
        // Show the one right after this card or inside it
        var targetId = $(this).data('target');
        $(targetId).slideToggle();
    });

    // Form Submission using AJAX
    $('#appointmentForm').on('submit', function(e) {
        e.preventDefault();

        // Basic Validation
        var phone = $('#phone').val();
        if(phone.length < 10){
            Swal.fire('Error', 'Please enter a valid phone number', 'error');
            return;
        }

        // Collect Data
        var formData = {
            pet_type: $('#petType').val(),
            pet_name: $('#petName').val(),
            owner_name: $('#ownerName').val(),
            phone: phone,
            email: $('#email').val(),
            city: $('#city').val(),
            date: $('#date').val(),
            branch: $('#branch').val(),
            message: $('#message').val()
        };

        // Send AJAX Request
        $.ajax({
            url: '/book_appointment',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                if(response.success) {
                    Swal.fire({
                        title: 'Success!',
                        text: response.message,
                        icon: 'success',
                        confirmButtonText: 'Great'
                    });
                    $('#appointmentForm')[0].reset(); // Reset form
                } else {
                    Swal.fire('Error', response.message, 'error');
                }
            },
            error: function() {
                Swal.fire('Error', 'Something went wrong. Please try again later.', 'error');
            }
        });
    });
});
