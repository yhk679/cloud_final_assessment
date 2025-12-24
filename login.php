<?php
$conn = new mysqli(
    "cloud-asg-database.c9qs6gxcc81n.us-east-1.rds.amazonaws.com",
    "admin",
    "admin123",
    "cloud_asg"
);

// Check DB connection
if ($conn->connect_error) {
    die("Database connection failed");
}

$username = $_POST['username'];
$password = $_POST['password'];

// Simple query (no hashing, for testing)
$sql = "SELECT * FROM users WHERE username=? AND password=?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $username, $password);
$stmt->execute();

$result = $stmt->get_result();

if ($result->num_rows === 1) {
    // Login success → redirect
    header("Location: index.html");
    exit;
} else {
    echo "❌ Login failed. Invalid username or password.";
}

$conn->close();
?>