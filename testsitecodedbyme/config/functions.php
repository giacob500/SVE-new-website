<?php
require_once 'db.php';

function display_data()
{
    global $con;
    $query = "select * from wp_orderinfo;";
    $result = mysqli_query($con, $query);
    return $result;
}

function filter_data($query)
{
    global $con;
    $filter_result = mysqli_query($con, $query);
    return $filter_result;
}


function look_for_data($lookingfor)
{
    global $con;
    // Create a template
    $query = "select * from wp_orderinfo where order_ID=?;";
    // Create a prepared statement
    $stmt = mysqli_stmt_init($con);
    // Prepare the prepared statement
    if (!mysqli_stmt_prepare($stmt, $query)) {
        echo "SQL statement failed";
        return $stmt;
    } else {
        // Bind parameters to the placeholder
        mysqli_stmt_bind_param($stmt, "i", $lookingfor);
        // Run parameters inside database
        mysqli_stmt_execute($stmt);
        $result = mysqli_stmt_get_result($stmt);
        return $result;
    }
}
