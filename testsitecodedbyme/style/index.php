<?php
require_once('../config/db.php');
require_once('../config/functions.php');

$result = display_data();

if (isset($_POST['search'])) {
    $valueToSearch = $_POST['valueToSearch'];
    $query = "SELECT * FROM `wp_orderinfo` WHERE `order_ID` = '$valueToSearch';";
    $search_result = filterTable($query);
} else {
    $query = "select * from wp_orderinfo;";
    $search_result = filterTable($query);
}

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
                <h4>Insert order into databse</h4>
                <form action="../includes/submit_insert.php" method="POST">
                    <div class="form-group">
                        <input class="form-control" type="text" name="id_to_insert" placeholder="Order ID">
                    </div>
                    <div class="form-group">
                        <input class="form-control" type="text" name="number_to_insert" placeholder="Order Quantity">
                    </div>
                    <div class="form-group">
                        <input class="form-control" type="text" name="name_to_insert" placeholder="Order Name">
                    </div>
                    <button class="btn btn-primary" type="submit" name="submit_insert">Insert</button>
                </form>
            </div>
            <div class="col">
                <h4>Remove order from databse</h4>
                <form action="../includes/submit_delete.php" method="POST">
                    <div class="form-group">
                        <input class="form-control" type="text" name="id_to_delete" placeholder="Order ID">
                    </div>
                    <button class="btn btn-danger" type="submit" name="submit_delete">Delete</button>
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
                    <button class="btn btn-secondary" type="submit" name="search">Submit</button>
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