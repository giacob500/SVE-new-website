<?php
require_once('../config/db.php');

$id = $_POST['id_to_delete'];

// Check filed is not empty
if (!empty($id)) {
    $query = "DELETE FROM `wp_orderinfo` WHERE `wp_orderinfo`.`order_ID` = $id;";
    mysqli_query($con, $query);
}

header("Location: ../style/index.php?submit_delete=success");
