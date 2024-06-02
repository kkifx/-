<?php
$dbhost = "localhost";
$dbname = "sqlitest";
$dbuser = "root";
$dbpass = "123456";
$conn = mysqli_connect($dbhost, $dbuser, $dbpass, $dbname);
$id = $_GET['id'];
echo $id;
$sql = "select * from news where id='$id'";
$result = mysqli_query($conn, $sql);
$row = mysqli_fetch_row($result);
echo 'id:' . $row['id'] . "<br>";
echo 'content:' . $row['content'] . "<br>";
?>
