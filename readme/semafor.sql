-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-05-2025 a las 11:17:31
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `semafor`
--
CREATE DATABASE IF NOT EXISTS `semafor` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `semafor`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `radar_deteccions`
--

CREATE TABLE `radar_deteccions` (
  `id` int(11) NOT NULL,
  `matricula` varchar(20) DEFAULT NULL,
  `velocitat` float DEFAULT NULL,
  `imatge_path` varchar(255) DEFAULT NULL,
  `processat_ocr` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `radar_deteccions`
--

INSERT INTO `radar_deteccions` (`id`, `matricula`, `velocitat`, `imatge_path`, `processat_ocr`, `timestamp`) VALUES
(1, '4C', 174.29, 'static/uploads\\captura_2025-05-23_09-59-22.jpg', 1, '2025-05-23 09:59:22'),
(2, 'C', 166.45, 'static/uploads\\captura_2025-05-23_10-10-53.jpg', 1, '2025-05-23 10:10:53'),
(3, '❌ No s\'ha detectat c', 161.95, 'static/uploads\\captura_2025-05-23_10-11-13.jpg', 1, '2025-05-23 10:11:13'),
(4, 'HCA', 160.09, 'static/uploads\\captura_2025-05-23_10-11-48.jpg', 1, '2025-05-23 10:11:48');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `created_at`) VALUES
(1, 'user1', 'scrypt:32768:8:1$qzFvqLBzUZc0kEc5$73e04810f634078303912b081d2cb53d9b4517b2da5e58f012acd2a93199ca4478cdd3bc8e132e3a648a95ac2643018e4f140be94decda347d8c3eb524af2bfd', 'test@gmail.com', '2025-05-13 20:53:25');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_old`
--

CREATE TABLE `users_old` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `radar_deteccions`
--
ALTER TABLE `radar_deteccions`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `users_old`
--
ALTER TABLE `users_old`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `radar_deteccions`
--
ALTER TABLE `radar_deteccions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `users_old`
--
ALTER TABLE `users_old`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
