<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

class SensorData {
    private $link = '';

    function __construct($temperature, $humidity, $id_dispositivo) {
        echo "Inicializando conexión...<br>";
        $this->connect();
        echo "Conexión exitosa...<br>";
        $this->storeInDB($temperature, $humidity, $id_dispositivo);
    }

    function connect() {
        $this->link = mysqli_connect('localhost', 'root', '') or die('Error al conectar a la base de datos');
        mysqli_select_db($this->link, 'esp32_data') or die('No se pudo seleccionar la base de datos');
    }

    function storeInDB($temperature, $humidity, $id_dispositivo) {
        echo "Almacenando datos: Temp = $temperature, Hum = $humidity, ID = $id_dispositivo<br>";

        $temperature = mysqli_real_escape_string($this->link, $temperature);
        $humidity = mysqli_real_escape_string($this->link, $humidity);
        $id_dispositivo = mysqli_real_escape_string($this->link, $id_dispositivo);

        $query = "INSERT INTO sensores (temperature, humidity, id_dispositivo) VALUES (?, ?, ?)";
        $stmt = mysqli_prepare($this->link, $query);

        if (!$stmt) {
            die("Error en la preparación de la consulta: " . mysqli_error($this->link));
        }

        mysqli_stmt_bind_param($stmt, 'dds', $temperature, $humidity, $id_dispositivo);

        if (mysqli_stmt_execute($stmt)) {
            echo "Dato guardado correctamente.<br>";
        } else {
            echo "Error al guardar los datos: " . mysqli_error($this->link) . "<br>";
        }

        mysqli_stmt_close($stmt);
    }

    function close() {
        mysqli_close($this->link);
    }
}

if (isset($_GET['temperature']) && isset($_GET['humidity']) && isset($_GET['id_dispositivo'])) {
    $temperature = $_GET['temperature'];
    $humidity = $_GET['humidity'];
    $id_dispositivo = $_GET['id_dispositivo'];

    if (is_numeric($temperature) && is_numeric($humidity) && !empty($id_dispositivo)) {
        $sensor = new SensorData($temperature, $humidity, $id_dispositivo);
    } else {
        echo "Datos inválidos.<br>";
    }
} else {
    echo "Faltan parámetros.<br>";
}
?>



