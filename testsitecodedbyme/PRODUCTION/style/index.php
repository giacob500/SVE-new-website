<?php
require_once('../config/db.php');
require_once('../config/functions.php');

$result = display_data();

function filterTable($query)
{
    global $con;
    $filter_Result = mysqli_query($con, $query);
    return $filter_Result;
}

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fetch data from database in PHP</title>
    <link rel="stylesheet" href="./bootstrap.min.css">
</head>

<body>
    <h1 class=text-center>Edit data in the database (POST method)</h1>
    <div class="container">
        <div class="row">
            <div class="col">
                <h4>Insert order into database</h4>
                <form action="../includes/submit_insert.php" method="POST">
                    <div class="form-group">
                        <?php
                        // The data filled in the "Order ID" field will not be lost when page is refreshed or updated
                        if (isset($_GET['id_to_insert'])) {
                            $id_to_insert = $_GET['id_to_insert'];
                            echo '<input class="form-control" type="text" name="id_to_insert" placeholder="Order ID" value="' . $id_to_insert . '">';
                        } else {
                            echo '<input class="form-control" type="text" name="id_to_insert" placeholder="Order ID">';
                        }
                        ?>
                    </div>
                    <div class="form-group">
                        <?php
                        // The data filled in the "Order Quantity" field will not be lost when page is refreshed or updated
                        if (isset($_GET['number_to_insert'])) {
                            $number_to_insert = $_GET['number_to_insert'];
                            echo '<input class="form-control" type="text" name="number_to_insert" placeholder="Order Quantity" value="' . $number_to_insert . '">';
                        } else {
                            echo '<input class="form-control" type="text" name="number_to_insert" placeholder="Order Quantity">';
                        }
                        ?>
                    </div>
                    <div class="form-group">
                        <?php
                        // The data filled in the "Order Name" field will not be lost when page is refreshed or updated
                        if (isset($_GET['name_to_insert'])) {
                            $name_to_insert = $_GET['name_to_insert'];
                            echo '<input class="form-control" type="text" name="name_to_insert" placeholder="Order Name" value="' . $name_to_insert . '">';
                        } else {
                            echo '<input class="form-control" type="text" name="name_to_insert" placeholder="Order Name">';
                        }
                        ?>
                    </div>
                    <button class="btn btn-primary" type="submit" name="submit_insert">Insert</button>
                </form>
                <?php
                // Check URL for strings establishing if request has failed
                if (!isset($_GET['submit_insert'])) {
                    // submit_insert has not been received from the server
                } else {
                    $insertCheck = $_GET['submit_insert'];
                    if ($insertCheck == "empty") {
                        echo "<p class='text-danger'>You did not fill in all fileds!<p>";
                        // exit(); <- it was inserted in the tutorial but I may not need it
                    } else if ($insertCheck == "error") {
                        echo "<p class='text-danger'>Submit request has not been sent!<p>";
                        // exit();
                    } else if ($insertCheck == "success") {
                        echo "<p class='text-success'>Data inserted successfully!<p>";
                        // exit();
                    }
                }
                ?>
            </div>
            <div class="col">
                <h4>Remove order from database</h4>
                <form action="../includes/submit_delete.php" method="POST">
                    <div class="form-group">
                        <input class="form-control" type="text" name="id_to_delete" placeholder="Order ID">
                    </div>
                    <button class="btn btn-danger" type="submit" name="submit_delete">Delete</button>
                </form>
                <?php
                // Check URL for strings establishing if request has failed
                if (!isset($_GET['submit_delete'])) {
                } else {
                    $deleteCheck = $_GET['submit_delete'];
                    if ($deleteCheck == "empty") {
                        echo "<p class='text-danger'>You did not fill the filed!<p>";
                        // exit(); <- it was inserted in the tutorial but I may not need it
                    } else if ($deleteCheck == "error") {
                        // submit_delete has not been received from the server
                        echo "<p class='text-danger'>Delete request has not been sent!<p>";
                        // exit();
                    } else if ($deleteCheck == "success") {
                        echo "<p class='text-success'>Delete request sent successfully!<p>";
                        // exit();
                    }
                }
                ?>
            </div>
        </div>
        <div class="card-body">
            <table class="table table-bordered text-center">
                <tr class="bg-dark text-white">
                    <td> Order ID </td>
                    <td> Order Counter </td>
                    <td> Order Name </td>
                </tr>
                <tr>
                    <?php
                    while ($row = mysqli_fetch_assoc($result)) {
                    ?>
                        <td><?php echo $row['order_ID']; ?></td>
                        <td><?php echo $row['order_counter']; ?></td>
                        <td><?php echo $row['order_names']; ?></td>
                </tr>
            <?php
                    };
            ?>
            </table>
        </div>
        <div class="row">
            <div class="col">
                <h4>Search in database</h4>
                <form action="index.php" method="POST">
                    <div class="form-group">
                        <input class="form-control" type="text" name="valueToSearch" placeholder="Order ID">
                    </div>
                    <button class="btn btn-secondary" type="submit" name="submit_search">Search</button>
                    <?php
                    if (isset($_POST['submit_search'])) {
                        $valueToSearch = $_POST['valueToSearch'];
                        //If pressed "Search" without filling the field
                        if (empty($valueToSearch)) {
                            $query = "SELECT * FROM `wp_orderinfo`;";
                            echo "<p class='text-danger'>You did not fill the filed!<p>";
                        } else {
                            $query = "SELECT * FROM `wp_orderinfo` WHERE `order_ID` = '$valueToSearch';";
                            echo "<p class='text-success'>Search request sent successfully!<p>";
                        }
                        $search_result = filterTable($query);
                    } else {
                        $query = "select * from wp_orderinfo;";
                        $search_result = filterTable($query);
                    }
                    ?>
                </form>
            </div>
        </div>
        <div class="card-body">
            <table class="table table-bordered text-center">
                <tr class="bg-dark text-white">
                    <td> Order ID </td>
                    <td> Order Counter </td>
                    <td> Order Name </td>
                </tr>
                <tr>
                    <?php while ($row2 = mysqli_fetch_array($search_result)) { ?>
                        <td><?php echo $row2['order_ID']; ?></td>
                        <td><?php echo $row2['order_counter']; ?></td>
                        <td><?php echo $row2['order_names']; ?></td>
                </tr>
            <?php }; ?>
            </table>
        </div>

    </div>
</body>

</html>