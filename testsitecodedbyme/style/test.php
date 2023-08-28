<?php
$con = mysqli_connect("localhost", "root", "", "testsite");

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['search'])) {
    $valueToSearch = $_POST['valueToSearch'];
    $query = "SELECT * FROM `wp_orderinfo` WHERE `order_ID` = '$valueToSearch'";
    $search_result = filterTable($query);
} else {
    $query = "SELECT * FROM wp_orderinfo";
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
    <h1 class="text-center">Find data in the database (POST method)</h1>
    <div class="container">
        <div class="card-body">
            <h4>Search in database</h4>
            <form action="test.php" method="POST">
                <div class="form-group">
                    <input class="form-control" type="text" name="valueToSearch" placeholder="Order ID">
                </div>
                <button class="btn btn-secondary" type="submit" name="search">Submit</button>
            </form>
            <table class="table table-bordered text-center">
                <tr class="bg-dark text-white">
                    <td> Order ID </td>
                    <td> Order Counter </td>
                    <td> Order Name </td>
                </tr>
                <?php while ($row2 = mysqli_fetch_array($search_result)) : ?>
                    <tr>
                        <td><?php echo $row2['order_ID']; ?></td>
                        <td><?php echo $row2['order_counter']; ?></td>
                        <td><?php echo $row2['order_names']; ?></td>
                    </tr>
                <?php endwhile; ?>
            </table>
        </div>
    </div>
</body>

</html>
