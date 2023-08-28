<?php
    $con = mysqli_connect("localhost", "root", "", "testsite");

    if(!$con){
        die("Connection failed: " . $conn->connect_error);
    }
?>