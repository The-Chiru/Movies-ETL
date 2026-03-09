# Movie ETL Pipeline

This project builds a simple ETL pipeline that processes the MovieLens dataset and enriches it with data from the OMDb API.

## Tech Stack

Python
PostgreSQL
Pandas
SQLAlchemy

## Data Sources

1. MovieLens Dataset
2. OMDb API

## Steps

1 Extract movie and rating data from CSV files
2 Enrich movie data using OMDb API
3 Transform and clean data
4 Load data into PostgreSQL database

## Setup

Install dependencies

pip install -r requirements.txt

Create database

CREATE DATABASE moviedb;

Run schema

psql -d moviedb -f schema.sql

Run ETL

python etl.py

## Challenges

API title mismatches and missing data were handled using exception handling and null values.

## Bonus Feature

Genres were normalized into separate tables for better relational design.
