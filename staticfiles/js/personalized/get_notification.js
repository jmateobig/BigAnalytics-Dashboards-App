$(document).ready(function() {
    // función para llamar al servicio de notificaciones
    function getNotifications() {
        $.ajax({
            url: '/notification/notification',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('.noti-icon-badge').text(data.length);

                var notificationsList = $('.noti-scroll');
                    for (var i = 0; i < data.length; i++) {
                     
                        var notification = data[i];
                        var description = notification.description;
                        var notificationItem = $('<a href="'+notification.url+'" class="dropdown-item notify-item" title="'+description+'"></a>');
                        var notifyIcon = $('<div class="notify-icon bg-primary"><i class="mdi mdi-comment-account-outline"></i></div>');
                        var notifyTitle = $('<h5 class="mt-0"></h5>');
                        var notifyDetails = $('<p class="notify-details"></p>');
                     
                        notifyDetails.html(description + '<br><small class="text-muted">' + notification.created_at+ '</small>');
                        notifyTitle.html(notification.title);
                        
                        notificationItem.append(notifyIcon);
                        notificationItem.append(notifyTitle);
                        notificationItem.append(notifyDetails);
                        notificationsList.append(notificationItem);
                    }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
    // llamamos a la función para obtener las notificaciones
    getNotifications();
});


$(document).ready(function () {
    // Asigna un evento de clic al enlace de notificaciones
    $("#notifications_content").click(function (e) {
        e.preventDefault();
        // Realiza una petición AJAX al método "View" del controlador
        $.ajax({
            type: "GET",
            url: '/notification/clear',
            success: function (result) {
                // Actualiza el número de notificaciones en el icono de notificaciones
                $('.noti-icon-badge').text("0");
            },
            error: function () {
            }
        });
    });
});