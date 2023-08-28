<?php
require_once('../config/db.php');

$query = "INSERT INTO wp_orderinfo (order_ID, order_counter, order_names)
        VALUES ('22222222', '22222222', '22222222');";
mysqli_query($con, $query);

header ("Location: ../style/index.php?submit_insert2=success");
?>