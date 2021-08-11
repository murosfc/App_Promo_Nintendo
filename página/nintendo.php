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
	echo "<h2>Site de Felipe Muros</h2> <br /> \n <h3>Luizinho é gay!</h3>";

	$result = mysqli_query($con,"SELECT * from db_nintendo_br, jogos_em_promo where db_nintendo_br.nsuid = jogos_em_promo.DB_Nintendo_BR_nsuid");

	echo "<table border='1'>
	<tr>
	<th>NSUID</th>
	<th>Título</th>
	<th>MSRP</th>
	<th>img_url</th>
	<th>Valor em Promoção</th>
	<th>Validade da promoção</th>
	</tr>";

	while($row = mysqli_fetch_array($result))
	{
	echo "<tr>";
	echo "<td>" . $row['nsuid'] . "</td>";
	echo "<td><h3>" . $row['titulo'] . "</h3></td>";
	echo "<td>R$ " . number_format($row['msrp'],2,',',' ') . "</td>";	
	echo "<td><img src=" . $row['img_url'] . "></td>";
	echo "<td>R$ " . number_format($row['sale_price'],2,',',' ') . "</td>";
	echo "<td>" . $row['validade_promo'] . "</td>";
	echo "</tr>";
	}
	echo "</table>";

	mysqli_close($con);
?>
