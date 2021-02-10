# A Django + Vue app for elearning

# A quick glance

This app is intended to be used as a tool for putting students' skills in a subject to test, as well as aiding them in preparing for an exam.

Teachers can create boards for their subject or course, add multiple-choice questions, and monitor the grades that students get.

Students can sign up to a course and take tests that are made up of randomly chosen questions among those added by teachers. There is full support for LaTeX in questions and answers texts.

Teachers can choose to have the questions for their course grouped in topics/categories and to have them appear in tests taken by students with a specific distribution (i.e., 2 questions from this category, 3 from the other one, and so on). They can moreover add assistants, that is users with the ability to add/edit questions for that course.

Finally, students will have a history of questions they have seen already, so they can review them, and a history of the tests they've taken, so they can monitor how they're doing over the longer term.

A more thorough documentation is being worked on currently. Please note that the code for this app uses English names and comments, but the app texts are in Italian.

# Features

- Ability for teachers to create courses and adjust settings such as the minimum passing score in tests, the number of points given for questions answered correctly/incorrectly/unanswered, the number of questions per tests, the categories/topics to divide questions into
    - Ability to also specify a distribution of questions in tests on a category basis: if your course has categories A, B, C, how many questions do you want to appear in tests from each one? (e.g 3 randomly picked questions from category A, 1 from B, 2 from C in each test)

- Ability for teachers to add "assistants" to their course, that is users with certain privileges that can aid in maintaining the course board by adding questions or editing existing ones
    - Assistants are based on a permission system that allows the admin of a course to choose, for each individual assistant, whether they have permissions for certain actions, such as: adding questions, editing questions, adding assistants, editing assistants' permissions

- Ability for students to sign up to multiple courses

- Ability for students to take tests made up of randomly chosen questions from the course they're taking the test, then view the results and the solutions and explanations for each question

- An erasable question history for students to keep track of the questions they've already seen in tests, as well as to prevent questions from appearing twice in subsequent ones

- A non-erasable history of tests taken by the student with all the details

- Additional features, both for students and teachers, to track performance over time
    - For example, teachers can see a list of the "hardest questions" for their course, that is those that have the highest percentage of wrong answers given relative to how many times they appeared in tests

# A couple screenshots
(Note: some screenshots may contain slightly different graphics such as a different color palette, as the user interface is still being worked on.)

## The teacher side

### Course control panel

![](https://i.imgur.com/fIeN4mY.png)

### Add/edit question views
![](https://i.imgur.com/vot6S9Q.png)
![](https://i.imgur.com/Qnbt6BS.png)

### Adding/editing assistants and permissions
(Click to watch the video)

[![Watch the video](https://img.youtube.com/vi/f3Ox_Z3dwY0/maxresdefault.jpg)](https://www.youtube.com/watch?v=f3Ox_Z3dwY0)

### Reporting errors in questions and handling reports
(Click to watch the video)

[![Watch the video](https://img.youtube.com/vi/N_nQqujdbM0/maxresdefault.jpg)](https://youtu.be/N_nQqujdbM0)

## The student side

### Course homepage
![](https://i.imgur.com/OVWVDQV.png)

### Taking tests
![](https://i.imgur.com/zDwCo28.png)
![](https://i.imgur.com/fnbCsSF.png)

### Question and test history
![](https://i.imgur.com/quprKH5.png)
![](https://i.imgur.com/8FeqEoO.png)

### Profile page
![](https://i.imgur.com/Do8k9vm.png)