<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") { 
    
    $name = isset($_POST['name']) ? trim($_POST['name']) : '';
    $email = isset($_POST['email']) ? trim($_POST['email']) : '';
    $message = isset($_POST['message']) ? trim($_POST['message']) : '';


    if ($name == '' || $email == '' || $message == '') {
        echo "Please fill in all fields.";
        exit;
    }

    $to = "youremail@example.com"; 
    $subject = "New Contact Form Message";
    $body = "Name: $name\nEmail: $email\nMessage:\n$message";
    $headers = "From: $email";

    if (mail($to, $subject, $body, $headers)) {
        echo "success";
    } else {
        echo "Error sending email. Please try again.";
    }
}
?>
