# FCSE-Skopje 2023 Undergraduate Study Programs Validator

This application is used to filter and validate the study programs and related courses from
the [Faculty of Computer Science and Engineering](https://finki.ukim.mk) at
the [Ss. Cyril and Methodius University in Skopje](https://www.ukim.edu.mk).
which can be found at the following [URL](https://finki.ukim.mk/mk/dodiplomski-studii).

## Prerequisites

- Data from
  the [undergraduate-study-program-etl](https://github.com/username-gigo-is-not-available/undergraduate-study-programs-scraper)
  is
  required to run this application.

## Overview

### Pipeline:

#### Study Program:

##### Loading Stage

- Load the study programs data (output from the etl) with the following columns:
  `study_program_id`, `study_program_code`, `study_program_name`, `study_program_duration`, `study_program_url`

##### Validating Stage

- Ensure `study_program_id` is a valid UUID
- Validate `study_program_code` follows the required pattern
- Confirm `study_program_url` is a valid URL
- Check that `study_program_duration` contains only allowed values

##### Storing Stage

- Store the validated data in a CSV file with the following
  columns: `study_program_id`, `study_program_code`, `study_program_name`, `study_program_duration`, `study_program_url`

#### Course:

##### Loading Stage

- Load the courses data (output from the etl) with the following columns:
  `course_id`, `course_code`, `course_name_mk`, `course_name_en`, `course_url`, `course_level`

##### Validating Stage

- Ensure `course_id` is a valid UUID
- Validate `course_code` follows the required pattern
- Confirm `course_url` is a valid URL
- Check that `course_level` contains only allowed values

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `course_id`, `course_code`, `course_name_mk`, `course_name_en`, `course_url`, `course_level`

#### Professor:

##### Loading Stage

- Load the professors data (output from the etl) with the following columns:
  `professor_id`, `professor_name`, `professor_surname`

##### Validating Stage

- Ensure `professor_id` is a valid UUID

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `professor_id`, `professor_name`, `professor_surname`

#### Curriculum:

##### Loading Stage

- Load the curricula data (output from the etl) with the following columns:
  `curriculum_id`, `course_type`, `course_semester`, `course_semester_season`, `course_academic_year`

##### Validating Stage

- Ensure `curriculum_id` is a valid UUID
- Check that `course_type` contains only allowed values
- Check that `course_semester_season` contains only allowed values
- Check that `course_academic_year` contains values in the allowed range
- Check that `course_semester` contains values in the allowed range

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `curriculum_id`, `course_type`, `course_semester`, `course_semester_season`, `course_academic_year`

#### Requisite:

##### Loading Stage

- Load the offers data (output from the etl) with the following columns:
  `requisite_id`, `course_prerequisite_type`, `minimum_required_number_of_courses`,

##### Validating Stage

- Ensure `requisite_id` is a valid UUID
- Check that `course_prerequisite_type` contains only allowed values
- Check that `minimum_required_number_of_courses` contains values in the allowed range

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `requisite_id`, `course_prerequisite_type`, `minimum_required_number_of_courses`,

#### Offers:

- Load the teaches data (output from the etl) with the following columns:
  `offers_id`, `curriculum_id`, `study_program_id`

##### Validating Stage

- Ensure `offers_id` is a valid UUID
- Verify that `study_program_id` exists in the study program dataset.
- Verify that `curriculum_id` exists in the curriculum dataset.

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `offers_id`, `curriculum_id`, `study_program_id`

#### Includes:

- Load the teaches data (output from the etl) with the following columns:
  `includes_id`, `curriculum_id`, `course_id`

##### Validating Stage

- Ensure `includes_id` is a valid UUID
- Verify that `course_id` exists in the course dataset.
- Verify that `curriculum_id` exists in the curriculum dataset.

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `includes_id`, `curriculum_id`, `course_id`

#### Requires:

##### Loading Stage

- Load the prerequisite data (output from the etl) with the following columns:
  `requires_id`, `requisite_id`, `course_id`

##### Validating Stage

- Ensure `requires_id` is a valid UUID
- Verify that `course_id` exists in the course dataset.
- Verify that `requisite_id` exists in the requisite dataset.

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `requires_id`, `requisite_id`, `course_id`

#### Satisfies:

##### Loading Stage

- Load the prerequisite data (output from the etl) with the following columns:
  `satisfies_id`, `requisite_id`, `prerequisite_course_id`

##### Validating Stage

- Ensure `satisfies_id` is a valid UUID
- Verify that `course_id` exists in the course dataset.
- Verify that `requisite_id` exists in the requisite dataset.

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `satisfies_id`, `requisite_id`, `prerequisite_course_id`

#### Teaches:

- Load the teaches data (output from the etl) with the following columns:
  `teaches_id`, `course_id`, `professor_id`

##### Validating Stage

- Ensure `teaches_id` is a valid UUID
- Verify that `professor_id` exists in the professor dataset.
- Verify that `course_id` exists in the course dataset.

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `teaches_id`, `course_id`, `professor_id`

### Results:

This application will produce the following datasets:

1. Study Programs: `study_program_id`, `study_program_code`, `study_program_name`, `study_program_duration`,
   `study_program_url`
2. Courses: `course_id`, `course_code`, `course_name_mk`, `course_name_en`, `course_url`
3. Professors: `professor_id`, `professor_name`, `professor_surname`
4. Curricula: `curriculum_id`, `course_type`, `course_semester_season`, `course_academic_year`, `course_semester`
5. Requisites: `requisite_id`, `course_prerequisite_type`, `minimum_required_number_of_courses`
6. Offers: `offers_id`, `curriculum_id`, `study_program_id`
7. Includes: `includes_id`, `curriculum_id`, `course_id`
8. Requires: `requires_id`, `requisite_id`, `course_id`
9. Satisfies: `satisfies_id`, `requisite_id`, `prerequisite_course_id`
10. Teaches: `teaches_id`, `course_id`, `professor_id`

## Requirements

- Python 3.9 or later

## Environment Variables

Before running the scraper, make sure to set the following environment variables:

- `FILE_STORAGE_TYPE`: the type of storage to use (either `LOCAL` or `MINIO`)

- `STUDY_PROGRAMS_DATA_INPUT_FILE_NAME`: the name of the study_programs input file
- `COURSE_DATA_INPUT_FILE_NAME`: the name of the courses input file
- `PROFESSORS_DATA_INPUT_FILE_NAME`: the name of the professors input file
- `CURRICULA_DATA_INPUT_FILE_NAME`: the name of the curricula input file
- `REQUISITES_DATA_INPUT_FILE_NAME`: the name of the requisites input file
- `OFFERS_DATA_INPUT_FILE_NAME`: the name of the offers input file
- `INCLUDES_DATA_INPUT_FILE_NAME`: the name of the includes input file
- `REQUIRES_DATA_INPUTT_FILE_NAME`: the name of the requires input file
- `SATISFIES_DATA_INPUT_FILE_NAME`: the name of the satisfies input file
- `TEACHES_DATA_INPUT_FILE_NAME`: the name of the teaches input file

- `STUDY_PROGRAMS_DATA_OUTPUT_FILE_NAME`: the name of the study_programs output file
- `COURSE_DATA_OUTPUT_FILE_NAME`: the name of the courses output file
- `PROFESSORS_DATA_OUTPUT_FILE_NAME`: the name of the professors output file
- `CURRICULA_DATA_OUTPUT_FILE_NAME`: the name of the curricula output file
- `REQUISITES_DATA_OUTPUT_FILE_NAME`: the name of the requisites output file
- `OFFERS_DATA_OUTPUT_FILE_NAME`: the name of the offers output file
- `INCLUDES_DATA_OUTPUT_FILE_NAME`: the name of the includes output file
- `REQUIRES_DATA_OUTPUT_FILE_NAME`: the name of the requires output file
- `SATISFIES_DATA_OUTPUT_FILE_NAME`: the name of the satisfies output file
- `TEACHES_DATA_OUTPUT_FILE_NAME`: the name of the teaches output file


##### If running the application with local storage:

- `INPUT_DIRECTORY_PATH`: the path to the directory where the input files are stored
- `OUTPUT_DIRECTORY_PATH`: the path to the directory where the output files will be saved

##### If running the application with MinIO:

- `MINIO_ENDPOINT_URL`: the endpoint of the MinIO server
- `MINIO_ACCESS_KEY`: the access key of the MinIO server
- `MINIO_SECRET_KEY`: the secret key of the MinIO server
- `MINIO_SOURCE_BUCKET_NAME`: the name of the bucket where the input files are stored
- `MINIO_DESTINATION_BUCKET_NAME`: the name of the bucket where the output files will be saved

## Installation

1. Clone the repository
    ```bash
    git clone <repository_url>
    ```

2. Install the required packages
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application
    ```bash
    python main.py
    ```

Make sure to replace `<repository_url>` with the actual URL of the repository.
