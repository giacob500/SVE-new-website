<?php
require_once('../config/db.php');

$id = $_POST['id'];
$number = $_POST['number'];
$name = $_POST['name'];

$query = "INSERT INTO wp_orderinfo (order_ID, order_counter, order_names)
        VALUES ('$id', '$number', '$name');";
mysqli_query($con, $query);

header ("Location: ../style/index.php?submit=success");
?>