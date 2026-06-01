DROP DATABASE IF EXISTS student_analyzer;
CREATE DATABASE student_analyzer;
USE student_analyzer;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role ENUM('student', 'teacher') NOT NULL
);

CREATE TABLE students (
    id INT PRIMARY KEY,
    class_name VARCHAR(50) NOT NULL,
    semester INT NOT NULL,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE teachers (
    id INT PRIMARY KEY,
    subject VARCHAR(100) NOT NULL,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    internal_marks INT DEFAULT 0,
    external_marks INT DEFAULT 0,
    semester INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    category ENUM('games', 'extra_activities') NOT NULL,
    file_path VARCHAR(255),
    points INT DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    teacher_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 10),
    remarks TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
);

INSERT INTO users (id, username, password_hash, name, role) VALUES 
(1, 'k_bumrah', 'scrypt:32768:8:1$xsXOIHA763iQPR4U$c798ac786895b6223ad797cb91da2b1aebd0cc222e4d0c35189ee9a2d4145e74689c37ad253289d950c572253f5987e8d5c49a44a4912b612794a7160a3c0768', 'Mr. Kuljinder', 'teacher'),
(2, 'k_padalia', 'scrypt:32768:8:1$xsXOIHA763iQPR4U$c798ac786895b6223ad797cb91da2b1aebd0cc222e4d0c35189ee9a2d4145e74689c37ad253289d950c572253f5987e8d5c49a44a4912b612794a7160a3c0768', 'Mr. Kamlesh ', 'teacher'),
(3, 'mayank', 'scrypt:32768:8:1$xsXOIHA763iQPR4U$c798ac786895b6223ad797cb91da2b1aebd0cc222e4d0c35189ee9a2d4145e74689c37ad253289d950c572253f5987e8d5c49a44a4912b612794a7160a3c0768', 'Mayank Karki', 'student'),
(4, 'prajwal', 'scrypt:32768:8:1$xsXOIHA763iQPR4U$c798ac786895b6223ad797cb91da2b1aebd0cc222e4d0c35189ee9a2d4145e74689c37ad253289d950c572253f5987e8d5c49a44a4912b612794a7160a3c0768', 'Prajwal Pandey', 'student'),
(5, 'ayushmona', 'scrypt:32768:8:1$xsXOIHA763iQPR4U$c798ac786895b6223ad797cb91da2b1aebd0cc222e4d0c35189ee9a2d4145e74689c37ad253289d950c572253f5987e8d5c49a44a4912b612794a7160a3c0768', 'Ayush Bisht', 'student');

INSERT INTO teachers (id, subject) VALUES 
(1, 'Mathematics'),
(2, 'Computer Science');

INSERT INTO students (id, class_name, semester) VALUES 
(3, 'Class 10', 1),
(4, 'Class 10', 1),
(5, 'Class 10', 2);

INSERT INTO marks (student_id, subject, internal_marks, external_marks, semester) VALUES 
(3, 'Mathematics', 18, 75, 1),
(3, 'Computer Science', 20, 85, 1),
(3, 'Physics', 15, 60, 1),
(4, 'Mathematics', 20, 90, 1),
(4, 'Computer Science', 19, 88, 1),
(4, 'Physics', 18, 80, 1),
(5, 'Mathematics', 12, 50, 2),
(5, 'Computer Science', 15, 65, 2);

INSERT INTO certificates (student_id, category, file_path, points) VALUES 
(3, 'games', 'mock_football.jpg', 10),
(3, 'extra_activities', 'mock_debate.pdf', 5),
(4, 'games', 'mock_basketball.jpg', 15);

INSERT INTO performance (student_id, teacher_id, rating, remarks) VALUES 
(3, 1, 8, 'Good performance, could improve in Physics.'),
(4, 2, 10, 'Excellent overall.'),
(5, 1, 5, 'Needs to focus more on studies.');
