-- Rode este arquivo no MySQL (terminal, Workbench ou phpMyAdmin) uma vez.
-- Na alwaysdata, apague as duas primeiras linhas e escolha o seu banco no phpMyAdmin.
CREATE DATABASE IF NOT EXISTS controle_equipamentos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE controle_equipamentos;

CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  login VARCHAR(50) NOT NULL UNIQUE,
  senha VARCHAR(100) NOT NULL            -- guarda o hash bcrypt, nunca a senha pura
);

CREATE TABLE IF NOT EXISTS categorias (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS fornecedores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  contato VARCHAR(150) NULL
);

CREATE TABLE IF NOT EXISTS equipamentos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  patrimonio VARCHAR(50) NULL UNIQUE,
  categoria_id INT NOT NULL,
  fornecedor_id INT NOT NULL,
  FOREIGN KEY (categoria_id) REFERENCES categorias(id),    -- não deixa apagar categoria em uso
  FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)  -- nem fornecedor em uso
);
