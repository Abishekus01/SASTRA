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

	"""
	Functional Dependencies
	=======================
	- `facutly_id` → `phone`, `salary`, `password`
	"""
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
	"""
	Functional Dependencies
	=======================
	- `student_id` → `section_id`
	"""
	cursor.execute("""CREATE TABLE IF NOT EXISTS `section_class` ( -- check section class capacity
				   `section_id` MEDIUMINT UNSIGNED NOT NULL,
				   `class_id` MEDIUMINT UNSIGNED NOT NULL,
				   PRIMARY KEY(`section_id`),
				   FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   UNIQUE(`class_id`)
	)""")
	"""
	Functional Dependencies
	=======================
	- `student_id` → `section_id`
	"""
	cursor.execute("""CREATE TABLE IF NOT EXISTS `section_students` ( -- check section class capacity
				   `section_id` MEDIUMINT UNSIGNED NOT NULL,
				   `student_id` INT UNSIGNED NOT NULL,
				   PRIMARY KEY(`student_id`),
				   FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	"""
	Functional Dependencies
	=======================
	- `id` → `faculty_id`, `section_id`, `course_id`
	- `faculty_id`, `section_id`, `course_id` → `id`
	"""
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
	"""
	Functional Dependencies
	=======================
	None Exist
	"""
	cursor.execute("""CREATE TABLE IF NOT EXISTS `student_electives` (
				   `student_id` INT UNSIGNED NOT NULL, -- check student is in this section,
				   `course_code` VARCHAR(10) NOT NULL, -- is this course elective of this student's programme?
				   PRIMARY KEY(`student_id`, `course_code`),
				   FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`)
				   ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	db_connector.commit()


# a.add_faculty(db, cursor, name="Lakshmi R",        campus_id=src_id, department="CSE", join_year=2015)
# a.add_faculty(db, cursor, name="Vijay Kumar",      campus_id=src_id, department="ECE", join_year=2012)
# a.add_faculty(db, cursor, name="Anita Sharma",     campus_id=src_id, department="Mathematics", join_year=2018)
# a.add_faculty(db, cursor, name="Rahul Menon", campus_id=src_id, department="Physics", join_year=2013)
# a.add_faculty(db, cursor, name="Priya Iyer",       campus_id=src_id, department="Chemistry", join_year=2016)

# Faculty info insertion
i.insert_faculty_info(s.db_connector, s.cursor, id=1, password="password1", phone="9876543210", salary=55000.00)
i.insert_faculty_info(s.db_connector, s.cursor, id=2, password="password2", phone="9765432109", salary=60000.00)
i.insert_faculty_info(s.db_connector, s.cursor, id=3, password="password3", phone="9654321098", salary=52000.00)
i.insert_faculty_info(s.db_connector, s.cursor, id=4, password="password4", phone="9543210987", salary=58000.00)
i.insert_faculty_info(s.db_connector, s.cursor, id=5, password="password5", phone="9432109876", salary=54000.00)

# One faculty teaching multiple courses (Lakshmi R → CSE101, CSE102)
i.insert_faculty_section_course(s.db_connector, s.cursor, faculty_id=1, section_id=1, course_code="CSE101")
i.insert_faculty_section_course(s.db_connector, s.cursor, faculty_id=1, section_id=1, course_code="CSE102")

# Multiple faculty teaching same course (CSE201 taught by Vijay Kumar and Anita Sharma)
i.insert_faculty_section_course(s.db_connector, s.cursor, faculty_id=2, section_id=2, course_code="CSE201")
i.insert_faculty_section_course(s.db_connector, s.cursor, faculty_id=3, section_id=3, course_code="CSE201")
