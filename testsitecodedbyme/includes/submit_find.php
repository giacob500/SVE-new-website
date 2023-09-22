<?php

if (isset($_POST['submit_search'])) {
    $valueToSearch = $_POST['valueToSearch'];
    // Check if field is empty
    if (empty($valueToSearch)){
        header("Location: ../style/index.php?submit_search=empty");
    } else {
        // The user filled the ID filed in the form
        header("Location: ../style/index.php?submit_search=success&valueToSearch=$valueToSearch");
    }   
} else {
    header("Location: ../style/index.php?submit_search=error");
}