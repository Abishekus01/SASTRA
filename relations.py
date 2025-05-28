from typehints import *
import database
import insert as i  # Assumes insert.py has insert_faculty, insert_faculty_info, etc.

def create_relations_and_insert_sample_data(db_connector: Connection, cursor: Cursor) -> None:
	"""
	Creates relational constraints and inserts sample data to test faculty-course-section mappings.
	"""
	# Step 1: Create base tables
	database.create_database(db_connector, cursor)

	# Step 2: Create relational tables

	cursor.execute("""CREATE TABLE IF NOT EXISTS `faculty_info` (
		`faculty_id` MEDIUMINT UNSIGNED,
		`phone` CHAR(10) NOT NULL,
		`salary` DECIMAL(12, 2) NOT NULL,
		`password` TINYTEXT NOT NULL,
		PRIMARY KEY(`faculty_id`),
		FOREIGN KEY(`faculty_id`) REFERENCES `faculties`(`id`)
		ON UPDATE CASCADE ON DELETE CASCADE,
		CHECK(`phone` REGEXP '^[6789][0-9]{9}$')
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS `section_class` (
		`section_id` MEDIUMINT UNSIGNED NOT NULL,
		`class_id` MEDIUMINT UNSIGNED NOT NULL,
		PRIMARY KEY(`section_id`),
		FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
		ON UPDATE CASCADE ON DELETE RESTRICT,
		FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`)
		ON UPDATE CASCADE ON DELETE RESTRICT,
		UNIQUE(`class_id`)
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS `section_students` (
		`section_id` MEDIUMINT UNSIGNED NOT NULL,
		`student_id` INT UNSIGNED NOT NULL,
		PRIMARY KEY(`student_id`),
		FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
		ON UPDATE CASCADE ON DELETE RESTRICT,
		FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
		ON UPDATE CASCADE ON DELETE RESTRICT
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS `faculty_section_course` (
		`id` INT UNSIGNED AUTO_INCREMENT,
		`faculty_id` MEDIUMINT UNSIGNED NOT NULL,
		`section_id` MEDIUMINT UNSIGNED NOT NULL,
		`course_code` VARCHAR(10) NOT NULL,
		PRIMARY KEY(`id`),
		FOREIGN KEY(`faculty_id`) REFERENCES `faculties`(`id`)
		ON UPDATE CASCADE ON DELETE RESTRICT,
		FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
		ON UPDATE CASCADE ON DELETE RESTRICT,
		FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`)
		ON UPDATE CASCADE ON DELETE RESTRICT,
		UNIQUE(`faculty_id`, `section_id`, `course_code`)
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS `student_electives` (
		`student_id` INT UNSIGNED NOT NULL,
		`course_code` VARCHAR(10) NOT NULL,
		PRIMARY KEY(`student_id`, `course_code`),
		FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
		ON UPDATE CASCADE ON DELETE RESTRICT,
		FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`)
		ON UPDATE CASCADE ON DELETE RESTRICT
	)""")

	# Step 3: Insert sample data

	# Add faculties
	i.insert_faculty(db_connector, cursor, id=101, name="Alice")
	i.insert_faculty(db_connector, cursor, id=102, name="Bob")
	i.insert_faculty(db_connector, cursor, id=103, name="Charlie")

	# Add faculty_info
	i.insert_faculty_info(db_connector, cursor, id=101, phone="9876543210", salary=50000, password="pass101")
	i.insert_faculty_info(db_connector, cursor, id=102, phone="8765432109", salary=52000, password="pass102")
	i.insert_faculty_info(db_connector, cursor, id=103, phone="7654321098", salary=51000, password="pass103")

	# Add sections
	i.insert_section(db_connector, cursor, id=201, name="S1")
	i.insert_section(db_connector, cursor, id=202, name="S2")
	i.insert_section(db_connector, cursor, id=203, name="S3")

	# Add courses
	i.insert_course(db_connector, cursor, code="CS101", name="Intro to CS", credits=3, is_lab=False)
	i.insert_course(db_connector, cursor, code="CS102", name="Data Structures", credits=4, is_lab=False)
	i.insert_course(db_connector, cursor, code="CS103", name="DBMS", credits=3, is_lab=False)

	# Insert into faculty_section_course
	sample_data = [
		(101, 201, "CS101"),  # Alice teaches CS101 in S1
		(101, 201, "CS102"),  # Alice teaches CS102 in S1
		(102, 202, "CS103"),  # Bob teaches CS103 in S2
		(103, 203, "CS103"),  # Charlie teaches CS103 in S3
	]

	for faculty_id, section_id, course_code in sample_data:
		try:
			cursor.execute(
				"""INSERT IGNORE INTO faculty_section_course
				(faculty_id, section_id, course_code)
				VALUES (%s, %s, %s)""",
				(faculty_id, section_id, course_code)
			)
		except Exception as e:
			print(f"Error inserting ({faculty_id}, {section_id}, {course_code}):", e)

	db_connector.commit()
