import { Component, OnInit } from '@angular/core';
import { CourseService, Course } from '../../course.service';

@Component({
  selector: 'app-course-list',
  standalone: false,
  templateUrl: './course-list.component.html',
  styleUrl: './course-list.component.css'
})
export class CourseListComponent implements OnInit {
  courses: Course[] = [];
  searchTerm = '';
  loading = true;
  error = '';

  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.loading = true;
    this.courseService.getCourses().subscribe({
      next: (posts) => {
        // Map JSONPlaceholder posts into course-shaped objects
        this.courses = posts.map((p, i) => ({
          id: p.id,
          name: p.title.slice(0, 24),
          code: `CS10${i + 1}`,
          credits: 3 + (i % 2),
          grade: 'A'
        }));
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load courses. Please try again.';
        this.loading = false;
      }
    });
  }

  get filteredCourses(): Course[] {
    return this.courses.filter((c) =>
      c.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
}
