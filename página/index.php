<?php
	$servername = "localhost";
	$username = "root";
	$password = "root";
	$database = "db_apppromonintendo";

	// Create connection
	$con = new mysqli($servername, $username, $password, $database);

	// Check connection
	if ($con->connect_error) {
	  die("Connection failed: " . $con->connect_error);
	}
	echo "<h2>Site de Felipe Muros</h2>";

	$result = mysqli_query($con,"SELECT * from db_nintendo_br, jogos_em_promo where db_nintendo_br.nsuid = jogos_em_promo.DB_Nintendo_BR_nsuid");	

	while($row = mysqli_fetch_array($result))
	{		
	echo "<p><h3>" . $row['titulo'] . "</h3></p>";
	echo "<p><img src=" . $row['img_url'] . "></p>";
	echo "<p>Valor cheio <s>R$ " . number_format($row['msrp'],2,',',' ') . "</s></p>";	
	echo "<p>Valor em promoção R$ " . number_format($row['sale_price'],2,',',' ') . "</p>";
	echo "<p>Desconto de <b>" . number_format((($row['msrp']-$row['sale_price'])/$row['msrp']*100),0,',',' ') . "%</b></p>";
	echo "<p> Promoção válida até " . $row['validade_promo'] . "</p>";
	echo "<br />";
	}	

	mysqli_close($con);
?>
