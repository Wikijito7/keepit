SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema keepit
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `keepit` ;

-- -----------------------------------------------------
-- Schema keepit
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `keepit` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `keepit` ;

-- -----------------------------------------------------
-- Table `keepit`.`Categorias`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `keepit`.`Categorias` ;

CREATE TABLE IF NOT EXISTS `keepit`.`Categorias` (
  `Nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Nombre`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `keepit`.`Etiquetas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `keepit`.`Etiquetas` ;

CREATE TABLE IF NOT EXISTS `keepit`.`Etiquetas` (
  `nombre` VARCHAR(45) NOT NULL,
  `id_etiquetas` INT NOT NULL auto_increment,
  PRIMARY KEY (`id_etiquetas`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `keepit`.`Notas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `keepit`.`Notas` ;

CREATE TABLE IF NOT EXISTS `keepit`.`Notas` (
  `id_notas` INT NOT NULL auto_increment,
  `titulo` VARCHAR(45) NULL,
  `contenido` TEXT NULL,
  `categoria` VARCHAR(45) NOT NULL,
  `Usuario_email` VARCHAR(75) NOT NULL,
  PRIMARY KEY (`id_notas`, `categoria`),
  INDEX `fk_Notas_Categoria_idx` (`categoria` ASC) VISIBLE,
  INDEX `fk_Notas_Usuario1_idx` (`Usuario_email` ASC) VISIBLE,
  CONSTRAINT `fk_Notas_Categoria`
    FOREIGN KEY (`categoria`)
    REFERENCES `keepit`.`Categorias` (`Nombre`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Notas_Usuario1`
    FOREIGN KEY (`Usuario_email`)
    REFERENCES `keepit`.`Usuario` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `keepit`.`Notas_has_Etiquetas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `keepit`.`Notas_has_Etiquetas` ;

CREATE TABLE IF NOT EXISTS `keepit`.`Notas_has_Etiquetas` (
  `Notas_id_notas` INT NOT NULL,
  `Etiquetas_id_etiquetas` INT NOT NULL,
  PRIMARY KEY (`Notas_id_notas`, `Etiquetas_id_etiquetas`),
  INDEX `fk_Notas_has_Etiquetas_Etiquetas1_idx` (`Etiquetas_id_etiquetas` ASC) VISIBLE,
  INDEX `fk_Notas_has_Etiquetas_Notas1_idx` (`Notas_id_notas` ASC) VISIBLE,
  CONSTRAINT `fk_Notas_has_Etiquetas_Notas1`
    FOREIGN KEY (`Notas_id_notas`)
    REFERENCES `keepit`.`Notas` (`id_notas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Notas_has_Etiquetas_Etiquetas1`
    FOREIGN KEY (`Etiquetas_id_etiquetas`)
    REFERENCES `keepit`.`Etiquetas` (`id_etiquetas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `keepit`.`Usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `keepit`.`Usuario` ;

CREATE TABLE IF NOT EXISTS `keepit`.`Usuario` (
  `email` VARCHAR(75) NOT NULL,
  `contrasena` VARCHAR(40) NULL,
  PRIMARY KEY (`email`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- USUARIO BASE DE DATOS --
CREATE USER 'keepit'@'localhost' IDENTIFIED BY 'keepit';
GRANT ALL PRIVILEGES ON * . * TO 'keepit'@'localhost';
FLUSH PRIVILEGES;
