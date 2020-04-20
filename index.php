<?php
$servername = "localhost";
$username = "root";
$password = "1987";
$dbname = "crawler";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
<!doctype html>
<html lang="en">

  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">

    <title>::. News Crawler .::</title>
  </head>
  <body>
    <div class="container">
		<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
			<a style="text-align:center" class="navbar-brand" href="#"> News Crawler of Asgaard Lab:   Topic: Covid-19</a>
			<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
				<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="navbarNavAltMarkup">
				<div class="navbar-nav">
				<!--
					<a class="nav-item nav-link active" href="#">Home <span class="sr-only">(current)</span></a>
					<a class="nav-item nav-link" href="#">Features</a> -->
				</div>
			</div>
		</nav>
		
		<hr />
		
		<div class="row">
			<div class="col">
			
				<div class="card">
					<div class="card-body">
						<form action="index.php" method="post" class="form-horizontal">
							<div class="form-row align-items-center">
								<div class="col-auto">
									<label class="sr-only" for="type">Name</label>
									<select name="type" class="form-control mb-2">
										<option value="">Select Type</option>
										<option value="cnn">CNN</option>
										<option value="dailystar">Daily Star</option>
									</select>
								</div>
								
								<div class="col-auto">
									<button type="submit" name="btn_news" class="btn btn-primary mb-2">Submit</button>
								</div>
							</div>
						</form>
					</div>
				</div>
				<?php if( isset( $_POST['btn_news'] ) ) { ?>
					<div class="card">
						<div class="card-header">
							<?php echo ucfirst( $_POST['type'] ); ?> News
						</div>
						
						<div class="card-body">
							<div class="table-responsive">
								<table class="table table-bordered table-hover">
									<thead class="thead-dark">
										<tr>
											<th scope="col">Sl. </th>
											<th scope="col">Title</th>
										</tr>
									</thead>
									<tbody>
									<?php
									$type = isset( $_POST['type'] ) ? $_POST['type'] : '';
									
									$sql = "SELECT * FROM news WHERE type= '". $type ."' ";

									$result = $conn->query($sql);

									if ($result->num_rows > 0) { ?>

									<?php
										$count = 1;
										// output data of each row
										while($row = $result->fetch_assoc()) { ?>
											<tr>
												<th scope="row"><?php echo $count; ?></th>
												<td>
													<p>
														<button class="btn" type="button" data-toggle="collapse" data-target="#new_description<?php echo $row['id']; ?>" aria-expanded="false" aria-controls="new_description">
															<?php echo $row['title']; ?>
														</button>
													<?php	header('Content-Type: text/html; charset=utf-8');
 echo (is_null($row['authors'])) ? "" : $row['authors']; ?>
													</p>
													<div class="collapse" id="new_description<?php echo $row['id']; ?>">
														<div class="card card-body">
															<?php header('Content-Type: text/html; charset=utf-8');
echo $row['description']; ?>
														</div>
													</div>
												</td>
											</tr>								
										<?php $count++; }
									} else {
										echo "Found 0 results.";
									}
									?>

									</tbody>
								</table>
							</div><!-- /table-responsive -->
						</div>
					</div><!-- /.card -->
				<?php } ?>
			</div><!-- /.col -->
		</div><!-- /.row -->
	</div><!-- /.container -->
	
	<?php $conn->close(); ?>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
  </body>
</html>
