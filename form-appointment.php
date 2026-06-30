<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = isset($_POST['name']) ? trim($_POST['name']) : '';
    $email = isset($_POST['email']) ? trim($_POST['email']) : '';
    $phone = isset($_POST['phone']) ? trim($_POST['phone']) : '';
    $date = isset($_POST['date']) ? trim($_POST['date']) : '';

    if ($name == '' || $email == '' || $phone == '' || $date == '') {
        echo "Please fill in all fields.";
        exit;
    }

    $to = "youremail@example.com"; 
    $subject = "New Appointment Request";
    $body = "Name: $name\nEmail: $email\nPhone: $phone\nDate: $date";
    $headers = "From: $email";

    if (mail($to, $subject, $body, $headers)) {
        echo "success";
    } else {
        echo "Error sending email. Please try again.";
    }
}
?>
