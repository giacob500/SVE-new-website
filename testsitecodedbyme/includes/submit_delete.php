<?php
require_once('../config/db.php');

$id = $_POST['id'];

$query = "DELETE FROM `wp_orderinfo` WHERE `wp_orderinfo`.`order_ID` = $id;";
mysqli_query($con, $query);

header ("Location: ../style/index.php?submit_delete=success");
?>