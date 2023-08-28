<?php
    require_once('../config/db.php');
    require_once('../config/functions.php');

    $result = display_data();
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
                <input class="form-control" type="text" name="id" placeholder="Order ID" >
            </div>
            <div class="form-group">
                <input class="form-control" type="text" name="number" placeholder="Order Quantity">
            </div>
            <div class="form-group">
                <input class="form-control" type="text" name="name" placeholder="Order Name">
            </div>
            <button class="btn btn-primary" type="submit" name="submit_insert">Submit</button>
        </form>
    </div>
    <div class="col">
    <h4>Remove order from databse</h4>
        <form action="../includes/submit_delete.php" method="POST">
            <div class="form-group">
                <input class="form-control" type="text" name="id" placeholder="Order ID" >
            </div>
            <button class="btn btn-danger" type="submit" name="submit_delete">Delete</button>
        </form>
    </div>
  </div>
        <div class="card-body">
            <h4>Database table</h4>
            <table class = "table table-bordered text-center">
                <tr class = "bg-dark text-white">
                    <td> Order ID </td>
                    <td> Order Counter </td>
                    <td> Order Name </td>
                </tr>
                <tr>
                <?php
                    while($row = mysqli_fetch_assoc($result))
                    {
                ?>
                    <td><?php echo $row['order_ID'];?></td>
                    <td><?php echo $row['order_counter'];?></td>
                    <td><?php echo $row['order_names'];?></td>
                </tr>
                <?php
                    }
                ?>
                </table>
                </div>
  </body>
</html>