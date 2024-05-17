# Smart PDF Sorter - Multi-Classifiers Batch Processor

## Overview
This Python application automates the classification and processing of PDF documents in batch mode using Azure AI Document Intelligence. It supports multiple classifiers, enabling efficient handling of various document types concurrently.

## Key Features
- **Batch Processing**: Allows for concurrent processing of multiple files to enhance efficiency.
- **Multi-Classifier Support**: Compatible with various classifiers for diverse document types.
- **Azure AI Integration**: Utilizes Azure AI Document Intelligence for accurate document classification and extraction.
- **Customizable Output**: Documents are sorted and saved into designated folders based on classification results.

## Prerequisites
Before you start, ensure you have the following:
- Python 3.8 or newer
- Azure AI Document Intelligence account
- Required Python packages installed:
  ```bash
  pip install PyPDF2 azure-core azure-ai-documentintelligence
