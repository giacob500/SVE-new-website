<?php

if (isset($_POST['search'])) {
    $valueToSearch = $_POST['valueToSearch'];
    header("Location: ../style/index.php?find_id=".$valueToSearch);
} else {
    header("Location: ../style/index.php?find_id=failed");
}

echo $id;


