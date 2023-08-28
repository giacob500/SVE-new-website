<?php
    require_once 'db.php';
    

    function display_data(){ 
        global $con;      
        $query = "select * from wp_orderinfo";
        $result = mysqli_query($con, $query);
        return $result;
    }
/*
    function insert_data(){
        global $con;
        $query = "INSERT INTO wp_orderinfo (order_ID, order_counter, order_names)
                VALUES ('3', '5', 'Mattonella 1, Mattonella2');";
        mysqli_query($con, $query);

        header ("Location: ../index.php?submit=success");
    }
    */
?>