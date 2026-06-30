<?php

/**
 * GrainGuys contact form handler.
 * Requires PHP mail() or SMTP on your hosting (not available on GitHub Pages).
 */

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo "Method not allowed.";
    exit;
}

// --- Configuration (update for your domain/host) ---
$toEmail = "info@grainguys.com";
$fromEmail = "noreply@grainguys.com";
$fromName = "GrainGuys Website";
$siteName = "GrainGuys";

$fname = isset($_POST["fname"]) ? trim($_POST["fname"]) : "";
$lname = isset($_POST["lname"]) ? trim($_POST["lname"]) : "";
$email = isset($_POST["email"]) ? trim($_POST["email"]) : "";
$phone = isset($_POST["phone"]) ? trim($_POST["phone"]) : "";
$message = isset($_POST["message"]) ? trim($_POST["message"]) : "";

if ($fname === "" || $lname === "" || $email === "" || $phone === "" || $message === "") {
    echo "Please fill in all fields.";
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo "Please enter a valid email address.";
    exit;
}

function h($value)
{
    return htmlspecialchars($value, ENT_QUOTES, "UTF-8");
}

$fullName = h($fname . " " . $lname);
$safeEmail = h($email);
$safePhone = h($phone);
$safeMessage = nl2br(h($message));
$submittedAt = date("j F Y, g:i a T");

$subject = "New contact form message — " . $fname . " " . $lname;

$htmlBody = <<<HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{$subject}</title>
</head>
<body style="margin:0;padding:0;background-color:#f4f4f4;font-family:Inter,Arial,sans-serif;color:#2D3C4C;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#f4f4f4;padding:32px 16px;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;width:100%;background-color:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(45,60,76,0.08);">
          <tr>
            <td style="background-color:#2D3C4C;padding:28px 32px;">
              <h1 style="margin:0;font-size:22px;line-height:1.3;color:#ffffff;">New contact enquiry</h1>
              <p style="margin:8px 0 0;font-size:14px;color:#CD9149;">{$siteName} website</p>
            </td>
          </tr>
          <tr>
            <td style="padding:32px;">
              <p style="margin:0 0 24px;font-size:15px;line-height:1.6;color:#555;">
                Someone submitted the contact form on your website. Details are below.
              </p>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid #eeeeee;font-size:13px;font-weight:600;color:#888;width:120px;">Name</td>
                  <td style="padding:12px 0;border-bottom:1px solid #eeeeee;font-size:15px;color:#2D3C4C;">{$fullName}</td>
                </tr>
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid #eeeeee;font-size:13px;font-weight:600;color:#888;">Email</td>
                  <td style="padding:12px 0;border-bottom:1px solid #eeeeee;font-size:15px;color:#2D3C4C;"><a href="mailto:{$safeEmail}" style="color:#CD9149;text-decoration:none;">{$safeEmail}</a></td>
                </tr>
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid #eeeeee;font-size:13px;font-weight:600;color:#888;">Phone</td>
                  <td style="padding:12px 0;border-bottom:1px solid #eeeeee;font-size:15px;color:#2D3C4C;"><a href="tel:{$safePhone}" style="color:#CD9149;text-decoration:none;">{$safePhone}</a></td>
                </tr>
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid #eeeeee;font-size:13px;font-weight:600;color:#888;vertical-align:top;">Message</td>
                  <td style="padding:12px 0;border-bottom:1px solid #eeeeee;font-size:15px;line-height:1.6;color:#2D3C4C;">{$safeMessage}</td>
                </tr>
                <tr>
                  <td style="padding:12px 0;font-size:13px;font-weight:600;color:#888;">Submitted</td>
                  <td style="padding:12px 0;font-size:14px;color:#888;">{$submittedAt}</td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="background-color:#fafafa;padding:20px 32px;border-top:1px solid #eeeeee;">
              <p style="margin:0;font-size:12px;line-height:1.5;color:#888;">
                Reply directly to this email to respond to {$fullName}.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
HTML;

$plainBody = "New contact form message\n\n"
    . "Name: {$fname} {$lname}\n"
    . "Email: {$email}\n"
    . "Phone: {$phone}\n\n"
    . "Message:\n{$message}\n\n"
    . "Submitted: {$submittedAt}\n";

$boundary = "=_GrainGuys_" . md5(uniqid((string) time(), true));

$headers = [
    "MIME-Version: 1.0",
    "From: {$fromName} <{$fromEmail}>",
    "Reply-To: {$fname} {$lname} <{$email}>",
    "Content-Type: multipart/alternative; boundary=\"{$boundary}\"",
    "X-Mailer: PHP/" . phpversion(),
];

$body = "--{$boundary}\r\n"
    . "Content-Type: text/plain; charset=UTF-8\r\n"
    . "Content-Transfer-Encoding: 8bit\r\n\r\n"
    . $plainBody . "\r\n"
    . "--{$boundary}\r\n"
    . "Content-Type: text/html; charset=UTF-8\r\n"
    . "Content-Transfer-Encoding: 8bit\r\n\r\n"
    . $htmlBody . "\r\n"
    . "--{$boundary}--";

if (mail($toEmail, $subject, $body, implode("\r\n", $headers))) {
    echo "success";
} else {
    echo "Error sending email. Please try again or call us directly.";
}
