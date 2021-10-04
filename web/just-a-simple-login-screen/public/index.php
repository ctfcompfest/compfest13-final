<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Just A Simple Login Screen</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  </head>
<?php
$failed = False;
$error = '';
if (($_SERVER['REQUEST_METHOD'] === 'POST') and ( !isset($_POST['username'], $_POST['password']))) {
  $error = 'Username and Password Required!';
  $failed = True;
} else if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  getenv('MYSQL_DBHOST') ? $db_host=getenv('MYSQL_DBHOST') : $db_host="localhost";
  getenv('MYSQL_DBPORT') ? $db_port=getenv('MYSQL_DBPORT') : $db_port="3306";
  getenv('MYSQL_DBUSER') ? $db_user=getenv('MYSQL_DBUSER') : $db_user="root";
  getenv('MYSQL_DBPASS') ? $db_pass=getenv('MYSQL_DBPASS') : $db_pass="root";
  getenv('MYSQL_DBNAME') ? $db_name=getenv('MYSQL_DBNAME') : $db_name="db";

  if (strlen( $db_name ) === 0)
    $conn = new mysqli("$db_host", $db_user, $db_pass);
  else
    $conn = new mysqli("$db_host", $db_user, $db_pass, $db_name);

  // Check connection
  if ($conn->connect_error) {
    $error = 'Connection failed: '.$conn->connect_error.'\n';
    $failed = True;
  }
} else {
  $failed = True;
}

if (!$failed) {
  $username = $_POST['username'];
  $password = $_POST['password'];
  if(preg_match('/\s/', $username)) {
    $error = 'Input Invalid!'; 
    $failed = True;
  }
  if(preg_match('/[\'"]/', $username)) {
    $error = 'Input Invalid!'; 
    $failed = True;
  }
  if(preg_match('/[\/\\\\]/', $username)) {
    $error = 'Input Invalid!';
    $failed = True;
  }
  if(preg_match('/(and|or|null|where|limit)/i', $username)) {
    $error = 'Input Invalid!'; 
    $failed = True;
  }
  if(preg_match('/(union|select|from|having)/i', $username)) {
    $error = 'Input Invalid!';
    $failed = True;
  }
  if(preg_match('/(group|order|having|limit)/i', $username)) {
    $error = 'Input Invalid!'; 
    $failed = True;
  }
  if(preg_match('/\s/', $password)) {
    $error = 'Input Invalid!'; 
    $failed = True;
  }
  if(preg_match('/[\'"]/', $password)) {
    $error = 'Input Invalid!';
    $failed = True;
  }
  if(preg_match('/[\/\\\\]/', $password)) {
    $error = 'Input Invalid!';
    $failed = True;
  }
  if(preg_match('/(and|or|null|where|limit)/i', $password)) {
    $error = 'Input Invalid!';
    $failed = True;
  }
  if(preg_match('/(union|select|from|having)/i', $password)) {
    $error = 'Input Invalid!';
    $failed = True;
  }
  if(preg_match('/(group|order|having|limit)/i', $password)) {
    $error = 'Input Invalid!'; 
    $failed = True;
  }
}

if (!$failed) {
  $sql = "SELECT username,pass FROM users WHERE username = $username AND pass = $password ";
  $result = mysqli_query($conn, $sql);
  if (!($result=mysqli_query($conn,$sql))) {
    if ($conn -> error) {
      $error = $conn -> error;
    }
    $failed = True;
  } else if ($result->num_rows == 0) {
    $error = 'Login Failed!';
    $failed = True;
  }
}

if ($failed) {
?>
  <nav class="navbar navbar-dark bg-primary">
      <span class="navbar-brand mb-0 h1">Meong</span>
  </nav>
  <div class="container align-items-center">
    <div class="d-flex justify-content-center mt-5">
      <img src="/images/meong.jpg" style="width: 250px; height: 200px; margin: auto;">
    </div>
  </div>
  <div class="container">
      <h1>Login</h1>
      <form action="" method="post">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" class="form-control" id="username" name="username" placeholder="Username">
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" class="form-control" id="password" name="password" placeholder="Password">
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </div>
      <div class="text-danger">
        <?php echo $error; ?>
      </div>
    </form>
<?php
} else {
  ?>
<nav class="navbar navbar-dark bg-primary">
      <span class="navbar-brand mb-0 h1">MeSUS</span>
  </nav>
  <div class="container align-items-center">
    <div class="d-flex justify-content-center mt-5">
      <img src="/images/mesus.png" style="width: 250px; height: 200px; margin: auto;">
    </div>
  </div>
  <div class="container align-items-center">
    <div class="d-flex justify-content-center mt-5">
      <h3>No Flag for you</h3>
    </div>
    <div class="d-flex justify-content-center">
      <p>You won't be able to get it. It's in a file /flag.txt</p>
    </div>
  </div>
<?php
}
?>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
  </body>
</html>