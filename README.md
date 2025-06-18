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
  `study_program_name`, `study_program_url`, `study_program_duration`

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
  `course_code`, `course_name_mk`, `course_name_en`, `course_url`

##### Validating Stage

- Ensure `course_id` is a valid UUID
- Validate `course_code` follows the required pattern
- Confirm `course_url` is a valid URL

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `course_id`, `course_code`, `course_name_mk`, `course_name_en`, `course_url`

#### Professor:

##### Loading Stage

- Load the professors data (output from the etl) with the following columns:
  `professor_id`, `professor_name`, `professor_surname`

##### Validating Stage

- Ensure `professor_id` is a valid UUID

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `professor_id`, `professor_name`, `professor_surname`

#### Teaches:

- Load the teaches data (output from the etl) with the following columns:
  `teaches_id`, `course_id`, `professor_id`

##### Filtering Stage

- Remove rows with `None` values in `professor_id`.

##### Validating Stage

- Verify that `professor_id` exists in the professor dataset.
- Verify that `course_id` exists in the course dataset.

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `teaches_id`, `course_id`, `professor_id`

#### Offers:

##### Loading Stage

- Load the offers data (output from the etl) with the following columns:
  `offers_id`, `study_program_id`, `course_id`, `course_type`, `course_semester`, 
  `course_semester_season`, `course_academic_year`, `course_level`

##### First pass (to filter out invalid prerequisites with depth = 1)

##### Merging Stage

- Left join with requires data on `course_id`
- Self left join on `study_program_id`, `course_prerequisite_id`, right on `study_program_id`, `course_id` with suffixes
  `_parent` and `_child`

##### Filtering Stage

- For type `ONE`: remove if the required course is not offered (`course_id_child` is `None`).
- For type `ANY`: group by (`study_program_id`, `course_id_parent`) and remove the row for the prerequisite that is not offered.
- For type `TOTAL`: group by (`study_program_id`, `course_id_parent`) and remove if the count of offered prerequisites is below the specified threshold (`minimum_required_number_of_courses`).

##### Renaming Stage

- Rename `course_id_parent` to `course_id`

##### Selecting Stage

- Select only the necessary columns for storage.

##### Second pass (to filter out invalid prerequisites with depth = 2)

##### Merging Stage

- Left join with requires data on `course_id`
- Self left join on `study_program_id`, `course_prerequisite_id`, right on `study_program_id`, `course_id` with suffixes
  `_parent` and `_child`

##### Filtering Stage

- For type `ONE`: remove if the required course is not offered (`course_id_child` is `None`).
- For type `ANY`: group by (`study_program_id`, `course_id_parent`) and remove the row for the prerequisite that is not offered.
- For type `TOTAL`: group by (`study_program_id`, `course_id_parent`) and remove if the count of offered prerequisites is below the specified threshold (`minimum_required_number_of_courses`).

##### Renaming Stage

- Rename `course_id_parent` to `course_id`

##### Selecting Stage

- Select only the necessary columns for storage.

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `offers_id`, `study_program_id`, `course_id`, `course_type`, `course_level`, `course_semester`,
  `course_semester_season`, `course_academic_year`,

#### Requires:

##### Loading Stage

- Load the offers data (output from the etl) with the following columns:
  `requires_id`, `course_id`, `course_prerequisite_type`, `course_prerequisites_course_id`,
  `minimum_required_number_of_courses`

##### Validating Stage

- Verify that `course_id` exists in the course dataset.
- Verify that each `course_prerequisite_id` exists in the course dataset.

##### Storing Stage

- Store the validated data in CSV files with the following columns:
  `requires_id`, `course_id`, `course_prerequisite_type`, `course_prerequisites_course_id`,
   `minimum_required_number_of_courses`


### Results:

This application will produce the following datasets:

1. Study Programs: `study_program_id`, `study_program_code`, `study_program_name`, `study_program_duration`,
   `study_program_url`
2. Courses: `course_id`, `course_code`, `course_name_mk`, `course_name_en`, `course_url`
3. Professors: `professor_id`, `professor_name`, `professor_surname`
4. Teaches: `teaches_id`, `course_id`, `professor_id`
5. Offers:  `offers_id`, `study_program_id`, `course_id`, `course_type`, `course_level`, `course_semester`,
   `course_semester_season`, `course_academic_year`,
6. Requires: `requires_id`, `course_id`, `course_prerequisite_type`, `course_prerequisites_course_id`,
   `minimum_required_number_of_courses`

## Requirements

- Python 3.9 or later

## Environment Variables

Before running the scraper, make sure to set the following environment variables:

- `FILE_STORAGE_TYPE`: the type of storage to use (either `LOCAL` or `MINIO`)
- `STUDY_PROGRAMS_INPUT_DATA_FILE_PATH`: the path to the study programs data file
- `CURRICULA_INPUT_DATA_FILE_PATH`: the path to the curricula data file
- `COURSE_INPUT_DATA_FILE_PATH`: the path to the courses data file
- `STUDY_PROGRAMS_DATA_OUTPUT_FILE_NAME`: the name of the study programs output file
- `COURSES_DATA_OUTPUT_FILE_NAME`: the name of the courses output file
- `PROFESSORS_DATA_OUTPUT_FILE_NAME`: the name of the professors output file
- `OFFERS_DATA_OUTPUT_FILE_NAME`: the name of the offers output file
- `TEACHES_DATA_OUTPUT_FILE_NAME`: the name of the teaches output file
- `REQUIRES_DATA_OUTPUT_FILE_NAME`: the name of the requires output file

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
