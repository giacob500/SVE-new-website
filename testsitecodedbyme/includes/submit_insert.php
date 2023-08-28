<?php
require_once('../config/db.php');

$id = mysqli_real_escape_string($con, $_POST['id_to_insert']);
$number = mysqli_real_escape_string($con, $_POST['number_to_insert']);
$name = mysqli_real_escape_string($con, $_POST['name_to_insert']);

// Check fileds are not empty
if (!empty($id) && !empty($number) && !empty($name)) {
$query = "INSERT INTO wp_orderinfo (order_ID, order_counter, order_names)
        VALUES (?, ?, ?);";
$stmt = mysqli_stmt_init($con);
if (!mysqli_stmt_prepare($stmt, $query)){
        echo "SQL error";
    } else {
        mysqli_stmt_bind_param($stmt, "sss", $id, $number, $name);
        mysqli_stmt_execute($stmt);
    }
}

header ("Location: ../style/index.php?submit_insert=success");
?>