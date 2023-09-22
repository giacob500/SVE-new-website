<?php
if (isset($_POST['submit_delete'])) {
    require_once('../config/db.php');

    $id = $_POST['id_to_delete'];

    // Check if field is empty
    if (empty($id)) {
        header("Location: ../style/index.php?submit_delete=empty");
    } else {
        // The user filled the ID filed in the form
        $query = "DELETE FROM `wp_orderinfo` WHERE `wp_orderinfo`.`order_ID` = $id;";
        mysqli_query($con, $query);
        header("Location: ../style/index.php?submit_delete=success");
    }
} else {
    header("Location: ../style/index.php?submit_delete=error");
}
