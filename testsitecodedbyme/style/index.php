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
        <h1>Reading data from database</h1>
        <div class="card-body">
            <table class = "table table-bordered text-center">
                <tr class = "bg-dark text-white">
                    <td> Order ID </td>
                    <td> Order Counter </td>
                    <td> Order Name </td>
                    <td> Delete </td>
                </tr>
                <tr>
                <?php
                    while($row = mysqli_fetch_assoc($result))
                    {
                ?>
                    <td><?php echo $row['order_ID'];?></td>
                    <td><?php echo $row['order_counter'];?></td>
                    <td><?php echo $row['order_names'];?></td>
                    <td><a href="#" class="btn btn-danger">Delete</td>
                </tr>
                <?php
                    }
                ?>
                </table>
                </div>
  </body>
</html>