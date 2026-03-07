# Work Intake Intelligence

## Overview
Work Intake Intelligence is a lightweight Applied AI / Analytics Engineering portfolio project focused on:
- intelligent work-item routing
- SLA risk prediction
- operations monitoring

The goal is to build a project that is:
- reproducible
- evaluable
- deployable
- monitorable
- interview-ready

## Problem
Operations teams often receive incoming tickets, requests, or work items from multiple channels. Manual triage can be slow and inconsistent, and SLA risk is often identified too late.

## Proposed Solution
This project will build a lightweight end-to-end workflow that:
1. predicts the likely routing queue for an incoming work item
2. predicts whether the work item is at risk of SLA breach
3. exposes a FastAPI `/predict` endpoint
4. supports lightweight monitoring for drift and score distribution changes
5. provides outputs for a Power BI operations dashboard

## Initial Technical Direction
- Python 3.11
- venv
- scikit-learn baseline models
- DuckDB
- FastAPI
- Power BI

## Baseline Strategy
- Routing model: TF-IDF + Logistic Regression
- SLA risk model: structured features + Logistic Regression

## Planned Deliverables
- synthetic dataset
- baseline training pipeline
- evaluation outputs
- FastAPI inference API
- monitoring report
- Power BI dashboard assets

## Current Status
Completed so far:
- local project initialization
- Git repository setup
- `.gitignore`
- virtual environment setup
- dependency installation

## Next Step
The next step is to define the synthetic data schema and generate the first version of project data.