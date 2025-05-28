from typehints import *

def create_relations(db_connector: Connection, cursor: Cursor) -> None:
	r"""
	Creates relational constraints for the database by defining additional relations.

	This function establishes foreign keys, uniqueness constraints, and checks on 
	relational tables that depend on the previously created schema.

	Parameters
	==========
	- **db_connector** : Connection
	  The database connection object used to interact with the database.

	- **cursor** : Cursor
	  A cursor object for executing SQL commands.

	Tables Created
	==============
	- **``faculty_info``**: Stores faculty phone, salary, and password.
	- **``section_class``**: Links sections to classrooms (non-labs).
	- **``section_students``**: Maps students to their sections.
	- **``faculty_section_course``**: Assigns faculties to teach courses in sections.
	- **``student_electives``**: Keeps track of students' elective course selections.

	Examples
	========
	.. code-block:: python

		>>> from SASTRA import *

		>>> # Create Connection object and Cursor object
		>>> connector, cursor = connect(
				user="root",
				password="secret_pwd",
				host="localhost"
			)
		
		>>> create_database(connector, cursor)
		>>> create_relations(connector, cursor)

	See Also
	========
	- `create_database()`: Defines base tables before relations are added.
	"""
	import database
	database.create_database(db_connector, cursor)

	# Table: faculty_info
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

	# Table: section_class
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

	# Table: section_students
	cursor.execute("""CREATE TABLE IF NOT EXISTS `section_students` (
		`section_id` MEDIUMINT UNSIGNED NOT NULL,
		`student_id` INT UNSIGNED NOT NULL,
		PRIMARY KEY(`student_id`),
		FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
		ON UPDATE CASCADE ON DELETE RESTRICT,
		FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
		ON UPDATE CASCADE ON DELETE RESTRICT
	)""")

	# Table: faculty_section_course
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

	# Table: student_electives
	cursor.execute("""CREATE TABLE IF NOT EXISTS `student_electives` (
		`student_id` INT UNSIGNED NOT NULL,
		`course_code` VARCHAR(10) NOT NULL,
		PRIMARY KEY(`student_id`, `course_code`),
		FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
		ON UPDATE CASCADE ON DELETE RESTRICT,
		FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`)
		ON UPDATE CASCADE ON DELETE RESTRICT
	)""")

	# ✅ Sample data insertion for testing multiple faculty-course-section combinations
	sample_data = [
		# Case 1: One faculty teaches two courses
		(101, 201, "CS101"),
		(101, 201, "CS102"),

		# Case 2: Same course taught by multiple faculty
		(102, 202, "CS103"),
		(103, 203, "CS103"),
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
